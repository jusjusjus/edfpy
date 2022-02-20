# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2022-02-20

### Added

- Reader API to read EDF files with minimal memory footprint

### Removed

- `EDF`
- `Header.build_channel_differences()`

## [0.1.1] - 2022-01-29

### Added

- gha for style/type/unit checks for py37,38,39,310
- this CHANGELOG
- test for `Header.build_channel_differences()`

### Changed

- pytest to v6.2.5

### Fixed

- add built channel differences also to `.sampling_rate_by_label`


[Unreleased]: https://github.com/jusjusjus/edfpy/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/jusjusjus/edfpy/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/jusjusjus/edfpy/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/jusjusjus/edfpy/releases/tag/v0.1.0
