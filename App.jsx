
import React,{useEffect,useState} from 'react';
const API=import.meta.env.VITE_API_URL||'http://127.0.0.1:8000';
const initial={area_sqft:1500,bedrooms:3,bathrooms:2,property_age:5,location:'Gurugram',parking:true,furnished:false};
export default function App(){
 const [f,S]=useState(initial),[r,R]=useState(null),[m,M]=useState(null),[err,E]=useState(''),[busy,B]=useState(false);
 useEffect(()=>{fetch(API+'/metrics').then(x=>x.json()).then(M).catch(()=>{});},[]);
 const set=(k,v)=>S(o=>({...o,[k]:v}));
 async function submit(e){e.preventDefault();B(true);E('');R(null);try{let q=await fetch(API+'/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...f,area_sqft:+f.area_sqft,bedrooms:+f.bedrooms,bathrooms:+f.bathrooms,property_age:+f.property_age})});let d=await q.json();if(!q.ok)throw Error(JSON.stringify(d.detail||d));R(d);}catch(x){E('Could not reach API. Start the backend first. '+x.message);}finally{B(false);}}
 return <div className="wrap"><nav><b>⌂ Estate<span>IQ</span></b><small>PROPERTY INTELLIGENCE</small></nav><header><label>✦ SMART PROPERTY VALUATION</label><h1>Know what your<br/><em>property is worth.</em></h1><p>Explore an illustrative property estimate powered by a machine-learning model.</p></header>
 <div className="grid"><form className="card" onSubmit={submit}><h2>Property details</h2><p className="sub">Enter the property information</p>
 {['area_sqft','bedrooms','bathrooms','property_age'].map((k)=><label className="field" key={k}>{({area_sqft:'Built-up area (sq. ft.)',bedrooms:'Bedrooms',bathrooms:'Bathrooms',property_age:'Property age (years)'})[k]}<input type="number" min={k==='area_sqft'?101:0} value={f[k]} onChange={e=>set(k,e.target.value)} required/></label>)}
 <label className="field">Location<select value={f.location} onChange={e=>set('location',e.target.value)}>{['Gurugram','Delhi','Noida','Sonipat','Jaipur','Bengaluru'].map(x=><option>{x}</option>)}</select></label>
 <div className="checks"><label><input type="checkbox" checked={f.parking} onChange={e=>set('parking',e.target.checked)}/> Parking</label><label><input type="checkbox" checked={f.furnished} onChange={e=>set('furnished',e.target.checked)}/> Furnished</label></div>
 <button disabled={busy}>{busy?'Calculating…':'Estimate property value →'}</button>{err&&<p className="error">{err}</p>}</form>
 <section><div className="card output"><small>ESTIMATED PROPERTY VALUE</small><h2>{r?r.formatted_price:'₹ —'}</h2>{r?<><p>{r.location} · {f.area_sqft} sq. ft.</p><div className="notice">{r.note}</div><h3>Top global model factors</h3>{r.key_factors.map(x=><div className="factor"><span>{x.feature.replaceAll('_',' ')}</span><b>{(x.importance*100).toFixed(1)}%</b><div className="track"><i style={{width:(x.importance*100)+'%'}}/></div></div>)}</>:<div className="placeholder">Your estimate will appear here after you submit the property details.</div>}</div>
 <div className="stats"><div className="card"><small>MODEL R²</small><strong>{m?m.r2.toFixed(3):'—'}</strong><p>Held-out demo data</p></div><div className="card"><small>TEST MAE</small><strong>{m?'₹'+(m.mae_inr/100000).toFixed(2)+'L':'—'}</strong><p>Mean absolute error</p></div></div></section></div>
 <aside>Educational demo using synthetic data only. Not a real market valuation or financial advice.</aside><footer>EstateIQ <span>React · FastAPI · scikit-learn</span></footer></div>
}
