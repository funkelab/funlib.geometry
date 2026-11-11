window.BENCHMARK_DATA = {
  "lastUpdate": 1794423723537,
  "repoUrl": "https://github.com/funkelab/funlib.geometry",
  "entries": {
    "funlib.geometry": [
      {
        "commit": {
          "author": {
            "name": "William Patton",
            "username": "pattonw",
            "email": "pattonw@hhmi.org"
          },
          "committer": {
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "bb008d20916f5acd8be39807aa7426b90ab4d93b",
          "message": "Merge pull request #9 from funkelab/docs-deploy-on-tags\n\nDeploy docs on version tags and by hand only",
          "timestamp": "2026-11-11T19:01:31Z",
          "url": "https://github.com/funkelab/funlib.geometry/commit/bb008d20916f5acd8be39807aa7426b90ab4d93b"
        },
        "date": 1794423722746,
        "tool": "customSmallerIsBetter",
        "benches": [
          {
            "name": "import funlib.geometry (cold)",
            "value": 10.13,
            "range": "± 0.219",
            "unit": "ms",
            "extra": "interpreter startup 7.3 ms subtracted; n=10"
          },
          {
            "name": "pytest wall time",
            "value": 0.607,
            "unit": "s",
            "extra": "`uv run pytest` in the tests job"
          }
        ]
      }
    ]
  }
}