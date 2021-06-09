Automated the pre-release steps for the release workflow

The release workflow for plugins now expects a release branch to exist with the correct 
.dev version and correct pulpcore requirements. The release workflow needs to be run
against the release branch being released. It takes one parameter: release tag (a.k.a
version string).
