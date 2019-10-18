# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project strives to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added
- Administrators can now configure process timeout values for web and vnc screenshot agent capabilities. ([#186](https://github.com/natlas/natlas/issues/186))

### Changed
- Screenshots are stored in deterministic location based purely on their file hash, instead of `timestamp/<hash>.ext`. ([#182](https://github.com/natlas/natlas/issues/182))

### Fixed

## [v0.6.6]

### Added
- Screenshot Browser ([#173](https://github.com/natlas/natlas/issues/173))
- Administrative settings:
    - Optionally use local subresources instead of CDN subresources (#[105](https://github.com/natlas/natlas/issues/105))
    - Optionally add a custom brand field to navigation to more easily identify the natlas instance you're viewing ([#106](https://github.com/natlas/natlas/issues/106))
- Store structured SSL certificate data for any port that we've identified an ssl-cert for ([#146](https://github.com/natlas/natlas/issues/146))

### Changed
- Agent logging is done via an app logger now with timestamps and to a file. ([#170](https://github.com/natlas/natlas/issues/170))
- Agent relies on nmap capabilities being set instead of running as root. ([#123](https://github.com/natlas/natlas/issues/123)) (Thanks droberson!)
- Agent refactoring to improve maintainability

### Fixed
- Handle NmapParserException when malformed xml files are encountered ([#169](https://github.com/natlas/natlas/issues/169))
- Improve randomness of `/random/` route by selecting a rand int each time instead of seeding with timestamp. ([#178]https://github.com/natlas/natlas/issues/178)

## [v0.6.5]
More information can be found at [natlas/v0.6.5](https://github.com/natlas/natlas/releases/tag/v0.6.5)

### Added
- Consolidate server logs into logs/ folder ([#163](https://github.com/natlas/natlas/issues/163))
- Logging scope manager and cyclical prng starts and restarts ([#118](https://github.com/natlas/natlas/issues/118))
- Screenshot filter ([#78](https://github.com/natlas/natlas/issues/78))
- Versioned Template Files ([#164](https://github.com/natlas/natlas/issues/164))
- Check For Update Feature ([#48](https://github.com/natlas/natlas/issues/48))
- Optional natlas version override for developing changes to the way host data is stored and presented. (No ticket)

### Changed
- Screenshot overhaul ([#72](https://github.com/natlas/natlas/issues/72))
	- Thumbnails of images
	- Save images on disk and serve as files (cacheable, less overhead than base64)
	- Serve thumbnail and only serve full image when clicked
	- nginx example location block included
	- serves from `$DOMAIN/media/`
- Load Search Modal Only When Clicked ([#141](https://github.com/natlas/natlas/issues/141))

### Fixed
- Failure to cleanup Aquatone files ([#157](https://github.com/natlas/natlas/issues/157))
- Screenshots Page Only Shows Most Recent Screenshots ([#98](https://github.com/natlas/natlas/issues/98))

## [v0.6.4]
More information can be found at [natlas/v0.6.4](https://github.com/natlas/natlas/releases/tag/v0.6.4)

### Added
* Server - Random button gives us a random host
* Server - User profiles can now select between different view formats (Currently supported: Pretty and Raw)
* Server - Added `tags` example to search help modal

### Changed
* Server - Automatically attempt to reconnect to elasticsearch on the next request if our last attempt failed and it's been more than 60 seconds.
* Server/Agent - `scan_id` field increased from 10 characters in length to 16 characters.

### Fixed
* Server - Fixed bug in scan manager ([#150](https://github.com/natlas/natlas/issues/150)) where updating the networks in range to scan caused unexpected scan targets.
* Server - Fixed view issue not populating user's settings in profile page
* Server - Cleanup relationship between a scope item and tags when a scope item is deleted
* Agent - Fixed retry failures when server is down so agents should now automatically try to reconnect as intended

## [v0.6.3]
More information can be found at [natlas/v0.6.3](https://github.com/natlas/natlas/releases/tag/v0.6.3)

### Added
* Normal users can now be added with the add-admin.py bootstrap script

### Changed
* SECURITY - Invite and Password Reset tokens have moved from using JWT to database-backed stateful tokens. These tokens expire after a defined period of time, as well as if the token is successfully used.
* Various styling improvements for authentication pages

### Fixed
* SECURITY - Invite and Password Reset flows have been updated to include an intermediary step that prevents the secret tokens from leaking to 3rd parties via the Referer header.
* SECURITY - Email validation is much stricter now, through the use of python-email-validator. This fixes problems where emails like `test@test.com@test.com` or `test @test.com` could have been treated as valid emails, causing unexpected behaviors.
* New users are explicitly created with "is_admin" set to false, instead of the previous "None" that they would get in certain flows.
* The nginx deployment script now correctly recommends placing all logs in the same folder, instead of `/var/log/nginx/natlas` and `/var/log/nginx/natlas.io`.
* Fixed erroneous help string in search help modal that was a holdover from v0.5.x.

### Removed
* Removed an unused css load from adobe for the NATLAS logo font. We previously settled on using the image, but had forgotten to remove the font stylesheet include.

## [v0.6.2]
More information can be found at [natlas/v0.6.2](https://github.com/natlas/natlas/releases/tag/v0.6.2)

### Added
* Branding improvements
* Version is now visible in the server footer
* Back-to-top button
* Server doesn't interact with mismatched versions

### Changed
* Style improvements
* Communication between agent and server has been more standardized around json messaging

### Fixed
* Agent standalone mode got broken with the agent configurations, fixed the standalone default scanning options

## [v0.6.1] - Bugfixes
More information can be found at [natlas/v0.6.1](https://github.com/natlas/natlas/releases/tag/v0.6.1)

### Fixed
* /api/natlas-services no longer breaks the admin page
* Extraneous debugging print statements removed


## [v0.6.0] - Structured data, better config, agent authn
More information can be found at [natlas/v0.6.0](https://github.com/natlas/natlas/releases/tag/v0.6.0)

### Added
* Server/Agent authentication using agent ID and secret
* Servers can assign tags to scope ranges
* Logged in users can request hosts to be rescanned, which puts them in a priority work queue
* XML parsing of nmap data to provide some structured elasticsearch data
* JSON export for scan results
* Agents can optionally ignore SSL validation warnings
* Agents can give themselves a maximum retry target before giving up a submit call to the server

### Changed
* jQuery and Bootstrap have been significantly upgraded to more modern versions
* Server setup script generates new random secret key if one doesn't already exist
* Move away from raw data view and into using the structured data
* Agents now report back to the server regardless if the host is up or not, which allows us to better track how many times we're actually scanning hosts.
* Tabled data now appears in DataTables, which allow for sorting, searching, and pagination

### Fixed
* Agents properly clean up scan data that were inadvertently left around when scans timeout
* Agents no longer request extra work for their local queue, resulting in extra data loss when agents are stopped
* Tons of HTML errors were corrected

## [v0.5.4] - Server stability improvements
More information can be found at [natlas/v0.5.4](https://github.com/natlas/natlas/releases/tag/v0.5.4)

### Fixed
* Setup-elastic now enables the elasticsearch systemd unit so that it survives reboots


## [v0.5.3] - Server setup improvements
More information can be found at [natlas/v0.5.3](https://github.com/natlas/natlas/releases/tag/v0.5.3)

### Changed
* Setup-server uses apt to install virtualenv instead of pip3

## [v0.5.2] - Server setup improvements
More information can be found at [natlas/v0.5.2](https://github.com/natlas/natlas/releases/tag/v0.5.2)

### Fixed
* Setup-server handles user creation correctly now

### Changed
* Setup-server changes ownership of the files to not be owned by root once finished setting up.

## [v0.5.1] - Agent bugfix, Responsive Views
More information can be found at [natlas/v0.5.1](https://github.com/natlas/natlas/releases/tag/v0.5.1)

### Changes
* Server has more responsive views

### Fixed
* Agent environment variables parse correctly now after correcting type casting


## [v0.5.0] - Initial Release
More Info can be found at [natlas/v0.5.0](https://github.com/natlas/natlas/releases/tag/v0.5.0)

### Server Added
* Automatic setup via setup scripts
* Server-side scripts for various management and bootstrap tasks
* Server-defined service database
* Server-defined agent config options
* Basic User-access controls
* Web service front end
* API agent access
* Example systemd and nginx deployment files

### Agent Added
* Use of nmap for port scans
* Headless web screenshots with [aquatone](https://github.com/michenriksen/aquatone)
* Headless VNC screenshots with vncsnapshot
* Configuration via .env file
* Ability to run in standalone mode


[Unreleased]: https://github.com/natlas/natlas/compare/v0.6.6...HEAD
[v0.6.6]: https://github.com/natlas/natlas/compare/v0.6.5...v0.6.6
[v0.6.5]: https://github.com/natlas/natlas/compare/v0.6.4...v0.6.5
[v0.6.4]: https://github.com/natlas/natlas/compare/v0.6.3...v0.6.4
[v0.6.3]: https://github.com/natlas/natlas/compare/v0.6.2...v0.6.3
[v0.6.2]: https://github.com/natlas/natlas/compare/v0.6.1...v0.6.2
[v0.6.1]: https://github.com/natlas/natlas/compare/v0.6.0...v0.6.1
[v0.6.0]: https://github.com/natlas/natlas/compare/v0.5.4...v0.6.0
[v0.5.4]: https://github.com/natlas/natlas/compare/v0.5.3...v0.5.4
[v0.5.3]: https://github.com/natlas/natlas/compare/v0.5.2...v0.5.3
[v0.5.2]: https://github.com/natlas/natlas/compare/v0.5.1...v0.5.2
[v0.5.1]: https://github.com/natlas/natlas/compare/v0.5.0...v0.5.1
[v0.5.0]: https://github.com/natlas/natlas/compare/v0.5.0