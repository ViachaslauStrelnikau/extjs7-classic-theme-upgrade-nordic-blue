from pathlib import Path
R=Path('D:/Projects/Extjs7ClassicThemeUpgradeNordicBlue');T=R/'tools/nordic-blue-acceptance'
s=(R/'TestApp/theme-lab/serve.cjs').read_text(encoding='utf-8-sig').replace("path.resolve(__dirname,'..')","path.resolve(__dirname,'../../TestApp')")
s=s.replace("const alias='/theme-lab/sdk/'","if(name==='/favicon.ico'){res.writeHead(204,{'Cache-Control':'no-store'});res.end();return}\n const alias='/theme-lab/sdk/'")
s=s.replace("server.listen(0,'127.0.0.1'","server.listen(51753,'127.0.0.1'")
(T/'serve.cjs').write_text(s,encoding='utf-8')
p=T/'native-pages.cjs';s=p.read_text(encoding='utf-8-sig');s=s.replace("base='http://127.0.0.1:51752/'","base=process.env.NORDIC_ACCEPTANCE_URL||'http://127.0.0.1:51753/'");p.write_text(s,encoding='utf-8')
print('Acceptance server: 51753; original 51752 unchanged')
