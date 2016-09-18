until python ./hourly_updater.py; do
    echo "Plotly crashed with exit code $?.  Respawning.." >&2
    sleep 1
done