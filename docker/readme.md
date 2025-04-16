 # login to ghcr.io
 echo {GITHUB_PAT} | docker login ghcr.io -u eml-henn --password-stdin

 the personal access token needs package read and write permissions. 
 
 docker build -t carbonitor .
 docker tag carbonitor:latest ghcr.io/henn-dt/carbonitor-v2/carbonitor:latest
 docker push ghcr.io/henn-dt/carbonitor-v2/carbonitor:latest

 build and push as oneliner:
 docker buildx build --tag ghcr.io/henn-dt/carbonitor-v2/carbonitor:latest --push .