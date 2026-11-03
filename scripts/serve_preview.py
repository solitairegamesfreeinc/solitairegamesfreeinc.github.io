#!/usr/bin/env python3
"""Local review only: loopback, no listing/dotfiles, truthful404 and noindex headers."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from urllib.parse import urlsplit,unquote
import functools,argparse
p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--port',type=int,required=True);p.add_argument('--spa-route',default='');args=p.parse_args();root=Path(args.root).resolve()
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  if any(s.startswith('.') for s in unquote(urlsplit(self.path).path).split('/') if s):return self.send_error(404)
  if args.spa_route and urlsplit(self.path).path.rstrip('/')==args.spa_route:self.path='/index.html'
  super().do_GET()
 def list_directory(self,path):self.send_error(404)
 def end_headers(self):
  self.send_header('X-Robots-Tag','noindex, follow');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Cache-Control','no-store');self.send_header('Referrer-Policy','strict-origin-when-cross-origin');super().end_headers()
 def send_error(self,code,message=None,explain=None):
  if code==404 and (root/'404.html').is_file():
   data=(root/'404.html').read_bytes();self.send_response(404);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers()
   if self.command!='HEAD':self.wfile.write(data)
  else:super().send_error(code,message,explain)
print('Local-only preview http://127.0.0.1:'+str(args.port)+'/',flush=True)
ThreadingHTTPServer(('127.0.0.1',args.port),functools.partial(Handler,directory=str(root))).serve_forever()
