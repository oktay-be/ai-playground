# Create conda env and activate it
conda create -n yazarca python=3.10.12
conda activate yazarca

pip install pip-tools==7.3.0
pip-compile requirements.in
pip install -r requirements.txt

conda info --envs
conda list -n yazarca