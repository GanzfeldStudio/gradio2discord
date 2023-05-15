import launch

if not launch.is_installed("discord"):
    launch.run_pip("install discord", "requirements 0 for Share-URL")
