Changed the handling of the latest release branch as a one off supported branch.

The ci_update_branches variable is now replaced by supported_release_branches and will not be touched by automation anymore.
However the latest_release_branch will be set by the create release branch workflow.
