#!/usr/bin/env python3
"""Check useful output, current download mappings and exact protected source bytes."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,hashlib,os,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/os.environ.get('BUILD_DIR','dist')
config=json.loads((ROOT/'site.config.json').read_text());build=json.loads((OUT/'.build.json').read_text());base=build['basePath'];errors=[]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.h1=0;self.structured=[];self.injson=False
 def handle_starttag(self,t,a):
  d=dict(a)
  if d.get('id'):self.ids.add(d['id'])
  if t=='h1':self.h1+=1
  if t=='a' and d.get('href'):self.links.append(d['href'])
  if t=='img' and 'alt' not in d:errors.append('Image alt missing')
  if t in ['script','img','link']:
   u=d.get('src',d.get('href',''))
   if u and d.get('rel')!='canonical':self.links.append(u)
  if t in ['source','img'] and d.get('srcset'):
   self.links.extend(candidate.strip().split()[0] for candidate in d['srcset'].split(','))
  if t=='script' and d.get('type')=='application/ld+json':self.injson=True
 def handle_endtag(self,t):
  if t=='script':self.injson=False
 def handle_data(self,s):
  if self.injson:
   try:self.structured.append(json.loads(s))
   except Exception as e:errors.append('Invalid JSON-LD '+str(e))
parsed={}
for f in OUT.rglob('*.html'):
 p=Page();p.feed(f.read_text());parsed[f]=p
for f,p in parsed.items():
 for href in p.links:
  u=urlsplit(href)
  if u.scheme or u.netloc:continue
  route=unquote(u.path)
  if base and route.startswith(base+'/'):route=route[len(base):]
  target=(OUT/route.lstrip('/')) if route.startswith('/') else ((f.parent/route) if route else f)
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(str(f.relative_to(OUT))+': missing '+href)
  elif u.fragment and target in parsed and u.fragment not in parsed[target].ids:errors.append('Missing anchor '+href)
for route in config['canonicalRoutes']:
 f=OUT/(route.strip('/')+'/index.html' if route.endswith('/') and route!='/' else ('index.html' if route=='/' else route.strip('/')))
 if not f.exists():errors.append('Missing canonical '+route);continue
 html=f.read_text();p=parsed[f]
 if route in config['managedRoutes'] and p.h1!=1:errors.append('Expected one managed H1 '+route)
 if config['canonical']+route not in html:errors.append('Canonical absent '+route)
 if build['mode']=='preview' and 'content="noindex,follow"' not in html:errors.append('Preview guard absent '+route)
for rel,digest in json.loads((ROOT/'evidence/preserved-files.json').read_text()).items():
 if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=digest:errors.append('Protected source changed '+rel)
 if (OUT/rel).exists() and not rel.endswith('.html') and (ROOT/rel).read_bytes()!=(OUT/rel).read_bytes():errors.append('Protected output changed '+rel)
for source,routes in config.get('frozenHtml',{}).items():
 for route in routes:
  if (ROOT/source).read_text() not in (OUT/route.strip('/')/'index.html').read_text():errors.append('Frozen legal fragment changed '+source+' in '+route)
# Keep exact original legal/support content while allowing wrapper-only security fixes.
for rel,record in json.loads((ROOT/'evidence/legal-content-preserved.json').read_text()).items():
 if record['preservedFragment'] not in (ROOT/rel).read_text():errors.append('Original legal content altered '+rel)
 if record['preservedFragment'] not in (OUT/rel).read_text():errors.append('Original legal output altered '+rel)
for f in OUT.rglob('*.html'):
 if re.search(r'<script[^>]+src=[\"\'][^\"\']*(?:vendor/(?:jquery|bootstrap)|new-age)',f.read_text(),re.I):errors.append('Retired theme script still loaded '+str(f.relative_to(OUT)))
locations=[e.text for e in ET.parse(OUT/'sitemap.xml').findall('.//{*}loc')]
if set(locations)!={config['canonical']+r for r in config['canonicalRoutes']}:errors.append('Wrong sitemap')

# Player-facing wrappers must expose their introduction without changing Unity assets.
for folder in config.get('visibleGameWrappers', []):
 html=(OUT/folder/'index.html').read_text()
 if 'id="about-game"' not in html or 'class="game-stage"' not in html:errors.append('Visible browser About panel absent '+folder)
 if re.search(r'left:\s*-\d{4,}px',html):errors.append('Offscreen browser content '+folder)
 if 'id="unity-canvas"' not in html:errors.append('Browser canvas absent '+folder)
for route,canonical in config.get('externalCanonicalAliases',{}).items():
 html=(OUT/route.strip('/')/'index.html').read_text()
 if 'rel="canonical" href="'+canonical+'"' not in html:errors.append('Cross-domain alias changed '+route)
 if config['canonical']+route in locations:errors.append('External canonical alias included in sitemap '+route)
if (OUT/'article.html').exists() and "'Last Updated: ' + article.updated" in (OUT/'article.html').read_text():errors.append('Fixed relative support age still rendered')
if build['mode']=='preview' and (OUT/'CNAME').exists():errors.append('Preview must not claim custom domain')
if (OUT/'app-ads.txt').read_bytes()!=(ROOT/'app-ads.txt').read_bytes():errors.append('Seller bytes changed')
report=dict(site=config['name'],mode=build['mode'],basePath=base,htmlPages=len(parsed),canonicalPages=len(locations),protectedFiles=len(json.loads((ROOT/'evidence/preserved-files.json').read_text())),errors=errors)
(ROOT/'evidence'/('validation-'+OUT.name+'.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(bool(errors))
