import setuptools

with open('README.rst') as fp:
    long_description = fp.read()

setuptools.setup(
    name='middlefield',
    license='MIT',
    description="Middlefield: A multifunctional tool.",
    long_description=long_description,
    use_incremental=True,
    setup_requires=['incremental'],
    author="Moshe Zadka",
    author_email="zadka.moshe@gmail.com",
    packages=setuptools.find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=['elcaminoreal', 'incremental', 'caparg',
                      'seashore', 'pex', 'toolz'],
    entry_points=dict(
        gather=["gather=middlefield"],
        console_scripts=["mf=middlefield._main:entrypoint"],
    )
)
