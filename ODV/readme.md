```bash
docker build -t gitlab-registry.ifremer.fr/repositories/public/odv:5.6.5 . 
docker run -p 6080:80  gitlab-registry.ifremer.fr/repositories/public/odv:5.6.5
```

Goto : <http://localhost:6080/>