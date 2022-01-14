Added the ``parallel_test_workers`` template_config.yml variable which defaults to 8. This variable
specifies the number of processes to run tests in parallel with. Tests can be marked as runnable in
parallel with the ``@pytest.mark.parallel`` decorator. Setting this variable to 0 disables parallel
running entirely.
