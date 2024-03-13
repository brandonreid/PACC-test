import time
from prefect import task, flow, pause_flow_run, prefect_runtime
from prefect.artifacts import create_markdown_artifact

@task(name="Get directory")
def get_directory():
    time.sleep(0.5)
    return 1

@task(name="Clone repo")
def clone_repo(num):
    time.sleep(2)
    return 1 + num

@task(name="Install dependencies")
def install_dependencies(num1, num2):
    time.sleep(6)
    return 1 + num1 + num2

@task(name="Build public")
def build_public():
    time.sleep(5)
    return 1

@task(name="Build config")
def build_config():
    time.sleep(2)
    markdown_content = """
    # Example Markdown Artifact
    """
    create_markdown_artifact(
        key="subflow-task-artifact",
        markdown=markdown_content,
        description="Subflow Task Test Artifact",
    )
    return 1

@task(name="Build")
def build_prod(num1):
    time.sleep(6)
    return 1 + num1

@flow(name="Build")
def build_app(num1, num2, num3):
    build_public.submit()
    config = build_config.submit()
    app = build_prod(config)
    markdown_content = """
    # Example Markdown Artifact
    """
    create_markdown_artifact(
        key="subflow-artifact",
        markdown=markdown_content,
        description="Subflow Test Artifact",
    )
    create_markdown_artifact(
        key="subflow-artifact-2",
        markdown=markdown_content,
        description="Subflow Test Artifact 2",
    )
    return app + num1 + num2 + num3

@task(name="Publish latest version")
def publish_latest(num1, num2):
    time.sleep(2.5)
    return 1 + num1 + num2

@task(name="Release")
def release_latest(num1, num2, num3):
    time.sleep(3)
    return 1 + num1 + num2 + num3

@task(name="Send notifications")
def send_notifications(num1, num2):
    time.sleep(1.8)
    return 1 + num1 + num2

@task(name="Cleanup", tags=["cleanup"])
def cleanup(num, num2):
    markdown_content = """
    # Example Markdown Artifact

    This is an *example* Markdown artifact created inline in a Prefect flow.

    ## Section

    - Item 1
    - Item 2
    """
    create_markdown_artifact(
        key="cleanup-task-artifact",
        markdown=markdown_content,
        description="Task Level Test Artifact",
    )
    create_markdown_artifact(
        markdown=markdown_content,
        description="Task Level Artifact with no key",
    )
    time.sleep(4)
    return 1 + num + num2

@flow(name="Nice flow with artifact")
def release_package():
    directory = get_directory.submit()
    repo = clone_repo.submit(directory)
    dependencies = install_dependencies.submit(directory, repo)
    app = build_app(directory, repo, dependencies)
    publish = publish_latest.submit(directory, app)
    release = release_latest.submit(directory, app, publish)
    send_notifications.submit(directory, release)
    cleanup.submit(directory, release)
    flow_name = prefect_runtime.flow_name
    name = pause_flow_run(str)
    markdown_content = f"""
    # Example Flow Run Level Markdown Artifact

    This is an *example* Markdown artifact created inline in a Prefect flow.

    ## The name was:
    {name}

    ## The flow name was:
    {flow_name}
    """
    create_markdown_artifact(
        key="cleanup-flow-artifact",
        markdown=markdown_content,
        description="Flow Level Test Artifact",
    )


if __name__ == "__main__":
    release_package()
