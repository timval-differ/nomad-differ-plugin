from nomad.config.models.north import NORTHTool
from nomad.config.models.plugins import NORTHToolEntryPoint

my_north_tool = NORTHTool(
    short_description='Jupyter Notebook server in NOMAD NORTH for NOMAD plugin nomad-differ-plugin.',
    image='ghcr.io/timval-differ/nomad-differ-plugin:main',
    description='Jupyter Notebook server in NOMAD NORTH for NOMAD plugin nomad-differ-plugin.',
    external_mounts=[],
    file_extensions=['ipynb'],
    icon='logo/jupyter.svg',
    image_pull_policy='Always',
    default_url='/lab',
    maintainer=[{'email': 't.j.j.vanalphen@differ.nl', 'name': 'Tim Differ'}],
    mount_path='/home/jovyan',
    path_prefix='lab/tree',
    privileged=False,
    with_path=True,
    display_name='my_north_tool',
)

north_entry_point = NORTHToolEntryPoint(
    id_url_safe='nomad-differ-plugin-my-north-tool',
    north_tool=my_north_tool,
)
