const http=require('http'),fs=require('fs'),path=require('path'),url=require('url');
const app=path.resolve(__dirname,'..'),sdk=path.resolve(app,'../ext-7.7.0.31');
function within(root,p){return p===root||p.startsWith(root+path.sep)}
const server=http.createServer((req,res)=>{
 let name;try{name=decodeURIComponent(url.parse(req.url).pathname)}catch(e){res.writeHead(400);res.end();return}
 if(name==='/favicon.ico'){res.writeHead(204,{'Cache-Control':'no-store'});res.end();return}
 const alias='/theme-lab/sdk/',isSdk=name.startsWith(alias),base=isSdk?sdk:app;
 if(name==='/')name='/modern-preview/index.html';
 const relative=isSdk?name.slice(alias.length):name.slice(1);
 const file=path.resolve(base,relative);
 if(!within(base,file)){res.writeHead(403);res.end();return}
 fs.readFile(file,(error,body)=>{if(error){res.writeHead(404);res.end('Missing resource');return}res.writeHead(200,{'Content-Type':({'.html':'text/html; charset=utf-8','.js':'application/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.gif':'image/gif','.woff':'font/woff','.woff2':'font/woff2','.ttf':'font/ttf'})[path.extname(file)]||'application/octet-stream','Cache-Control':'no-store'});res.end(body)});
});
server.listen(51754,'127.0.0.1',()=>console.log('http://127.0.0.1:'+server.address().port+'/modern-preview/index.html'));
