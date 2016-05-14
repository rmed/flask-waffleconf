# Changelog

## 0.3.0 - May 14th, 2016

### Added

- SQLAlchemy support (`AlchemyWaffleStore`)
- Update notifications using file timestamp
- Extension methods to call in views
- New configuration variables (`WAFFLE_WATCHTYPE`, `WAFFLE_WATCHER_FILE`)
- Data (de)serialization

### Changed

- Structure of the `WAFFLE_CONFS` dict is now simpler:
    - Only `desc` and `default` are required
- Extension no longer requires a custom template or view (see documentation for
  new implementation)
- Documentation rewritten and migrated to Sphinx

### Deprecated

- `gevent` support (bad implementation)
- `WAFFLE_TEMPLATE` setting no longer used

## 0.2.0 - August 25th, 2015

### Added

- Support for multiprocess deployments using Redis and `threading` or `gevent`

### Changed

- `WaffleConf` object no longer stores application and store

### Fixed

- Typo in default form template

## 0.1.0 - August 19th, 2015

- Initial release
- Support for single process deployments
