#!/usr/bin/env python3
"""Build existing static company pages without running the retired theme toolchain."""
import hashlib,json,os,re,shutil,subprocess
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'site.config.json').read_text())
MODE=os.environ.get('SITE_MODE','preview')
NAME=os.environ.get('BUILD_DIR','dist')
BASE=os.environ.get('BASE_PATH','').rstrip('/')
if MODE not in ['preview','production'] or NAME not in ['dist','dist-production','dist-subpath']:
 raise SystemExit('Use preview/production and a supported dist directory')
if '..' in BASE:raise SystemExit('Unsafe BASE_PATH')
if BASE and not re.fullmatch(r'/[A-Za-z0-9/_-]+',BASE):raise SystemExit('Unsafe BASE_PATH')
OUT=ROOT/NAME
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir()
allowed=set(CONFIG['publicDirectories'])
for item in ROOT.iterdir():
 if item.is_dir() and item.name in allowed:shutil.copytree(item,OUT/item.name)
 elif item.is_file() and (item.suffix.lower() in ['.html','.ico','.png','.svg','.webmanifest'] or item.name in ['app-ads.txt','llms.txt']+CONFIG.get('publicFiles',[])):shutil.copy2(item,OUT/item.name)
canonical=CONFIG['canonical'].rstrip('/')
for file in OUT.rglob('*.html'):
 rel=file.relative_to(OUT).as_posix();route='/'+(rel[:-10] if rel.endswith('index.html') else rel)
 if route=='/index.html':route='/'
 html=file.read_text()
 html=re.sub(r'<meta\s+name=[\"\']robots[\"\'][^>]*>','',html,flags=re.I)
 noindex=MODE=='preview' or rel in CONFIG.get('noindexFiles',[]) or rel=='404.html'
 robots='noindex,follow' if noindex else 'index,follow,max-snippet:-1,max-image-preview:large'
 additions=f'<meta name="robots" content="{robots}">'
 if not re.search(r'<link[^>]+rel=[\"\']canonical',html,re.I):additions+=f'<link rel="canonical" href="{canonical+route}">'
 if not re.search(r'<meta[^>]+name=[\"\']description',html,re.I):additions+='<meta name="description" content="'+CONFIG['name']+' information, privacy and support.">'
 html=html.replace('</head>',additions+'</head>',1)
 if BASE:
  html=re.sub(r'((?:href|src|action)=([\"\']))(/(?!/))',lambda m:m[1]+BASE+m[3],html)
 if BASE:
  html=re.sub(r'(srcset=([\"\']))(.*?)(\2)',lambda m:m[1]+re.sub(r'(^|,)(\s*)/(?!/)',lambda n:n[1]+n[2]+BASE+'/',m[3])+m[4],html)
  html=html.replace('content="0;url=/','content="0;url='+BASE+'/')
 file.write_text(html)
# Retain both older .html legal routes and extensionless directory destinations.
for alias,source in CONFIG.get('contentAliases',{}).items():
 target=OUT/alias.strip('/');target.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(OUT/source,target/'index.html')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+canonical+'/sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+canonical+route+'</loc></url>' for route in CONFIG['canonicalRoutes'])+'</urlset>\n')
(OUT/'.nojekyll').touch()
if MODE=='production' and not BASE:(OUT/'CNAME').write_text(urlsplit(canonical).hostname+'\n')
try:revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
except Exception:revision='uncommitted'
(OUT/'.build.json').write_text(json.dumps(dict(mode=MODE,basePath=BASE,revision=revision,canonical=canonical)))
print(json.dumps(dict(site=CONFIG['name'],output=str(OUT),mode=MODE,basePath=BASE,canonicalPages=len(CONFIG['canonicalRoutes']))))
