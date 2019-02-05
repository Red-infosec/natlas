from flask import render_template, redirect, url_for, current_app, flash, Response, abort
from flask_login import current_user
from app import db
from app.admin import bp
from app.admin.forms import UserDeleteForm, UserEditForm, InviteUserForm, \
    NewScopeForm, ImportScopeForm, ImportBlacklistForm, ScopeToggleForm, ScopeDeleteForm
from app.models import User, ScopeItem
from app.auth.email import send_user_invite_email
from app.auth.wrappers import isAuthenticated, isAdmin
import ipaddress

@bp.route('/', methods=['GET'])
@isAuthenticated
@isAdmin
def admin():
    if current_user.is_admin:
        return render_template("admin/index.html")
    else:
        flash("You're not an admin!", 'danger')
        return redirect(url_for('main.index'))


@bp.route('/users', methods=['GET', 'POST'])
@isAuthenticated
@isAdmin
def users():
    if current_user.is_admin:
        users = User.query.all()
        delForm = UserDeleteForm()
        editForm = UserEditForm()
        inviteForm = InviteUserForm()
        if inviteForm.validate_on_submit():
            newUser = User(email=inviteForm.email.data)
            db.session.add(newUser)
            send_user_invite_email(newUser)
            db.session.commit()
            flash('Invitation Sent!', 'success')
            return redirect(url_for('admin.users'))
        return render_template("admin/users.html", users=users, delForm=delForm, editForm=editForm, inviteForm=inviteForm)
    else:
        flash("You're not an admin!", 'danger')
        return redirect(url_for('main.index'))


@bp.route('/users/<int:id>/delete', methods=['POST'])
@isAuthenticated
@isAdmin
def deleteUser(id):
    if current_user.is_admin:
        delForm = UserDeleteForm()
        if delForm.validate_on_submit():
            if current_user.id == id:
                flash('You can\'t delete yourself!', 'danger')
                return redirect(url_for('admin.users'))
            user = User.query.filter_by(id=id).first()
            User.query.filter_by(id=id).delete()
            db.session.commit()
            flash('%s deleted!' % user.email, 'success')
            return redirect(url_for('admin.users'))
        else:
            flash("Form couldn't validate!", 'danger')
            return redirect(url_for('admin.users'))
    else:
        flash("You're not an admin!", 'danger')
        return redirect(url_for('main.index'))


@bp.route('/users/<int:id>/toggle', methods=['POST'])
@isAuthenticated
@isAdmin
def toggleUser(id):
    if current_user.is_admin:
        editForm = UserEditForm()
        if editForm.validate_on_submit():
            user = User.query.filter_by(id=id).first()
            if user.is_admin:
                admins = User.query.filter_by(is_admin=True).all()
                if len(admins) == 1:
                    flash('Can\'t delete the last admin!', 'danger')
                    return redirect(url_for('admin.users'))
                user.is_admin = False
                db.session.commit()
                flash('User demoted!', 'success')
                return redirect(url_for('admin.users'))
            else:
                user.is_admin = True
                db.session.commit()
                flash('User promoted!', 'success')
                return redirect(url_for('admin.users'))
        else:
            flash("Form couldn't validate!", 'danger')
            return redirect(url_for('admin.users'))
    else:
        flash("You're not an admin!", 'danger')
        return redirect(url_for('main.index'))


@bp.route('/scope', methods=['GET', 'POST'])
@isAuthenticated
@isAdmin
def scope():
    scope = ScopeItem.getScope()
    scopeSize = current_app.ScopeManager.getScopeSize()
    if scopeSize == 0: # if it's zero, let's update the app's scopemanager
        current_app.ScopeManager.update()
        scopeSize = current_app.ScopeManager.getScopeSize() # if it's zero again that's fine, we just had to check
    newForm = NewScopeForm()
    delForm = ScopeDeleteForm()
    editForm = ScopeToggleForm()
    importForm = ImportScopeForm()
    if newForm.validate_on_submit():
        if '/' not in newForm.target.data:
            newForm.target.data = newForm.target.data + '/32'
        target = ipaddress.ip_network(newForm.target.data, False)
        newTarget = ScopeItem(target=target.with_prefixlen, blacklist=False)
        db.session.add(newTarget)
        db.session.commit()
        current_app.ScopeManager.updateScope()
        flash('%s added!' % newTarget.target, 'success')
        return redirect(url_for('admin.scope'))
    return render_template("admin/scope.html", scope=scope, scopeSize=scopeSize, delForm=delForm, editForm=editForm, newForm=newForm, importForm=importForm)


@bp.route('/blacklist', methods=['GET', 'POST'])
@isAuthenticated
@isAdmin
def blacklist():
    if current_user.is_admin:
        scope = ScopeItem.getBlacklist()
        blacklistSize = current_app.ScopeManager.getBlacklistSize()
        newForm = NewScopeForm()
        delForm = ScopeDeleteForm()
        editForm = ScopeToggleForm()
        importForm = ImportBlacklistForm()
        if newForm.validate_on_submit():
            if '/' not in newForm.target.data:
                newForm.target.data = newForm.target.data + '/32'
            target = ipaddress.ip_network(newForm.target.data, False)
            newTarget = ScopeItem(target=target.with_prefixlen, blacklist=True)
            db.session.add(newTarget)
            db.session.commit()
            current_app.ScopeManager.updateBlacklist()
            flash('%s blacklisted!' % newTarget.target, 'success')
            return redirect(url_for('admin.blacklist'))
        return render_template("admin/blacklist.html", scope=scope, blacklistSize=blacklistSize, delForm=delForm, editForm=editForm, newForm=newForm, importForm=importForm)
    else:
        flash("You're not an admin!", 'danger')
        return redirect(url_for('main.index'))


@bp.route('/import/<string:scopetype>', methods=['POST'])
@isAuthenticated
@isAdmin
def importScope(scopetype=''):
    if current_user.is_admin:
        if scopetype == 'blacklist':
            importBlacklist = True
            importForm = ImportBlacklistForm()
        elif scopetype == 'scope':
            importBlacklist = False
            importForm = ImportScopeForm()
        else:
            abort(404)
        if importForm.validate_on_submit():
            successImport = []
            alreadyExists = []
            failedImport = []
            newScopeItems = importForm.scope.data.split('\n')
            for item in newScopeItems:
                item = item.strip()
                if '/' not in item:
                    item = item + '/32'
                try:
                    target = ipaddress.ip_network(item, False)
                except ValueError as e:
                    failedImport.append(item) # this item couldn't be validated as an ip network
                    continue
                exists = ScopeItem.query.filter_by(target=target.with_prefixlen).first()
                if exists:
                    alreadyExists.append(target.with_prefixlen) # this range is already a scope item
                    continue
                newTarget = ScopeItem(target=target.with_prefixlen, blacklist=importBlacklist)
                db.session.add(newTarget)
                successImport.append(newTarget.target)
            db.session.commit()
            current_app.ScopeManager.update()
            if len(successImport) > 0:
                flash('%s targets added to %s!' % (len(successImport), scopetype), 'success')
            if len(alreadyExists) > 0:
                flash('%s targets already existed!' % len(alreadyExists), 'info')
            if len(failedImport) > 0:
                flash('%s targets failed to import!' % len(failedImport), 'danger')
                for item in failedImport:
                    flash('%s' % item, 'danger')
            return redirect(url_for('admin.%s' % scopetype))
        else:
            for field, errors in importForm.errors.items():
                for error in errors:
                    flash(error, 'danger')
            return redirect(url_for('admin.%s' % scopetype))
    else:
        flash("You're not an admin!", 'danger')
        return redirect(url_for('main.index'))

@bp.route('/export/<string:scopetype>', methods=['GET'])
@isAuthenticated
@isAdmin
def exportScope(scopetype=''):
    if current_user.is_admin:
        if scopetype == 'blacklist':
            exportBlacklist = True
        elif scopetype == 'scope':
            exportBlacklist = False
        else:
            abort(404)
        items = ScopeItem.query.filter_by(blacklist=exportBlacklist).all()
        return Response('\n'.join(str(item.target) for item in items), mimetype='text/plain')
    else:
        flash("You're not an admin!", 'danger')
        return redirect(url_for('main.index'))

@bp.route('/scope/<int:id>/delete', methods=['POST'])
@isAuthenticated
@isAdmin
def deleteScopeItem(id):
    if current_user.is_admin:
        delForm = ScopeDeleteForm()
        if delForm.validate_on_submit():
            item = ScopeItem.query.filter_by(id=id).first()
            if item.blacklist:
                redirectLoc = 'admin.blacklist'
            else:
                redirectLoc = 'admin.scope'
            ScopeItem.query.filter_by(id=id).delete()
            db.session.commit()
            current_app.ScopeManager.update()
            flash('%s deleted!' % item.target, 'success')
            return redirect(url_for(redirectLoc))
        else:
            flash("Form couldn't validate!", 'danger')
            return redirect(url_for(redirectLoc))
    else:
        flash("You're not an admin!", 'danger')
        return redirect(url_for('main.index'))


@bp.route('/scope/<int:id>/toggle', methods=['POST'])
@isAuthenticated
@isAdmin
def toggleScopeItem(id):
    if current_user.is_admin:
        toggleForm = ScopeToggleForm()
        if toggleForm.validate_on_submit():
            item = ScopeItem.query.filter_by(id=id).first()
            if item.blacklist:
                item.blacklist = False
                redirectLoc = 'admin.blacklist'
                flash('%s removed from blacklist!' % item.target, 'success')
            else:
                item.blacklist = True
                redirectLoc = 'admin.scope'
                flash('%s blacklisted!' % item.target, 'success')
            db.session.commit()
            current_app.ScopeManager.update()
            return redirect(url_for('admin.scope'))
        else:
            flash("Form couldn't validate!", 'danger')
            return redirect(url_for('admin.scope'))
    else:
        flash("You're not an admin!", 'danger')
        return redirect(url_for('main.index'))