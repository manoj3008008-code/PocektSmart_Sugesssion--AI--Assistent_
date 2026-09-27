async function api(url, options={}) {
  const r = await fetch(url, {credentials:"include", ...options});
  let data={}; try{data=await r.json()}catch{}
  if(!r.ok){return {detail:data.detail||"Request failed", status:r.status}}
  return data;
}
function showMessage(text, ok=false){
  const el=document.querySelector("#formMessage");
  if(el){el.className=ok?"success":"error";el.textContent=text}
}
function bindJsonForm(id,url,redirect){
  const form=document.getElementById(id); if(!form)return;
  form.addEventListener("submit",async e=>{
    e.preventDefault();
    const data=Object.fromEntries(new FormData(form).entries());
    const r=await api(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
    if(r.detail){showMessage(r.detail);return}
    showMessage("Success",true); if(redirect)setTimeout(()=>location=redirect,300);
  });
}
function renderResult(data){
  const box=document.querySelector("#result");
  if(!box)return;
  box.innerHTML=`<div class="panel"><p class="eyebrow">${data.planner.toUpperCase()} RECOMMENDATIONS</p><h2>${escapeHtml(data.summary)}</h2>
  <p>Budget: ₹${Number(data.budget).toLocaleString("en-IN")} · Estimated allocation: ₹${Number(data.allocated_total).toLocaleString("en-IN")}</p>
  <div class="result-grid">${(data.items||[]).map(x=>`<div class="result-card"><h3>${escapeHtml(x.name)}</h3><small>${escapeHtml(x.category)} · ${escapeHtml(x.platform)}</small><div class="price">₹${Number(x.estimated_price).toLocaleString("en-IN")}</div><p>${escapeHtml(x.reason)}</p><a href="${x.search_url}" target="_blank" rel="noopener">Search platform →</a></div>`).join("")}</div>
  <h3>Tips</h3>${(data.tips||[]).map(t=>`<p class="tip">• ${escapeHtml(t)}</p>`).join("")}<p class="muted">${escapeHtml(data.disclaimer||"")}</p></div>`;
}
function escapeHtml(v){return String(v??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]))}
function bindPlanner(id,url,planner){
  const form=document.getElementById(id); if(!form)return;
  form.addEventListener("submit",async e=>{
    e.preventDefault();
    let options={method:"POST"};
    if(planner==="jewelry"){options.body=new FormData(form)}
    else {
      const raw=Object.fromEntries(new FormData(form).entries());
      if(planner==="home"){
        try{raw.rooms=raw.rooms.split(",").map(x=>x.trim()).filter(Boolean);raw.items=JSON.parse(raw.items)}
        catch{document.querySelector("#result").innerHTML='<div class="panel error">Items must be valid JSON.</div>';return}
      }
      raw.budget=Number(raw.budget); if(planner==="party")raw.guests=Number(raw.guests);
      options.headers={"Content-Type":"application/json"};options.body=JSON.stringify(raw);
    }
    const r=await api(url,options); if(r.detail){document.querySelector("#result").innerHTML=`<div class="panel error">${escapeHtml(r.detail)}</div>`;return}
    renderResult(r); window.scrollTo({top:document.querySelector("#result").offsetTop-80,behavior:"smooth"});
  });
}
async function logout(){await api("/api/logout",{method:"POST"});location="/login"}
