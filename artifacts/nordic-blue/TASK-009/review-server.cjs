// Read-only loopback review server; compatible with the Cmd-bundled Node runtime.
const http=require('http'),fs=require('fs'),path=require('path'),url=require('url'),zlib=require('zlib'),crypto=require('crypto');
const root=path.resolve(__dirname,'..');
const zip=fs.readFileSync(path.join(__dirname,'evidence.zip')),entries={};
const expected=JSON.parse(fs.readFileSync(path.join(__dirname,'evidence-index.json'),'utf8')).archiveSha256;
if(crypto.createHash('sha256').update(zip).digest('hex')!==expected)throw Error('Evidence archive checksum mismatch');
let eocd=zip.length-22;
while(eocd>=Math.max(0,zip.length-65557)&&zip.readUInt32LE(eocd)!==0x06054b50)eocd--;
if(eocd<0)throw Error('Missing ZIP directory');
let offset=zip.readUInt32LE(eocd+16),count=zip.readUInt16LE(eocd+10);
for(let n=0;n<count;n++){
 if(zip.readUInt32LE(offset)!==0x02014b50)throw Error('Invalid ZIP entry');
 const len=zip.readUInt16LE(offset+28),extra=zip.readUInt16LE(offset+30),comment=zip.readUInt16LE(offset+32);
 const name=zip.slice(offset+46,offset+46+len).toString('utf8');
 entries[name]={method:zip.readUInt16LE(offset+10),size:zip.readUInt32LE(offset+20),local:zip.readUInt32LE(offset+42)};offset+=46+len+extra+comment;
}
function archived(key){const item=entries[key];if(!item)return null;const start=item.local+30+zip.readUInt16LE(item.local+26)+zip.readUInt16LE(item.local+28),body=zip.slice(start,start+item.size);if(item.method===0)return body;if(item.method===8)return zlib.inflateRawSync(body);throw Error('Unsupported ZIP method');}
const server=http.createServer((req,res)=>{
 let pathname;try{pathname=decodeURIComponent(url.parse(req.url).pathname);}catch(e){res.writeHead(400);res.end();return;}
 if(pathname==='/'){res.writeHead(302,{Location:'/TASK-009/review.html'});res.end();return;}
 const file=path.resolve(root,'.'+pathname);
 if(file.indexOf(root+path.sep)!==0){res.writeHead(403);res.end();return;}
 fs.readFile(file,(error,body)=>{if(error){body=pathname.indexOf('/TASK-009/')===0?archived(pathname.slice('/TASK-009/'.length)):null;if(!body){res.writeHead(404);res.end('Missing');return;}}
  res.writeHead(200,{'Content-Type':{'.html':'text/html; charset=utf-8','.png':'image/png','.json':'application/json; charset=utf-8','.md':'text/plain; charset=utf-8','.css':'text/css','.js':'application/javascript'}[path.extname(file)]||'application/octet-stream','Cache-Control':'no-store'});res.end(body);
 });
});
server.listen(0,'127.0.0.1',()=>process.stdout.write('http://127.0.0.1:'+server.address().port+'/TASK-009/review.html\n'));
