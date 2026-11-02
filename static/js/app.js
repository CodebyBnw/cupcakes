document.addEventListener('DOMContentLoaded',()=>{
  // Filtro em tempo real (US03)
  document.querySelectorAll('[data-filtro]').forEach(b=>b.addEventListener('click',e=>{
    e.preventDefault();const f=b.dataset.filtro;
    document.querySelectorAll('[data-filtro]').forEach(x=>x.classList.toggle('on',x===b));
    document.querySelectorAll('.produto').forEach(c=>{c.hidden=f!==''&&c.dataset.restricao!==f});
  }));
  // Subtotal dinamico do cupcake (US02)
  document.querySelectorAll('.produto form').forEach(fm=>{
    const out=fm.querySelector('.subtotal'),qt=fm.querySelector('[name=qt]'),pr=fm.querySelector('[name=premium]'),base=parseFloat(fm.dataset.preco);
    const calc=()=>{out.textContent=((base+(pr.checked?2:0))*(parseInt(qt.value)||1)).toFixed(2).replace('.',',')};
    qt.addEventListener('input',calc);pr.addEventListener('change',calc);calc();
  });
  // Seletor de quantidade
  document.querySelectorAll('.qtd').forEach(q=>{const i=q.querySelector('input'),max=parseInt(i.dataset.max);
    const set=v=>{i.value=Math.max(1,Math.min(max,v));i.dispatchEvent(new Event('input'))};
    q.querySelector('.menos').onclick=()=>set(+i.value-1);q.querySelector('.mais').onclick=()=>set(+i.value+1)});
  // Mascara de CEP (US08)
  const cep=document.querySelector('[name=cep]');
  if(cep)cep.addEventListener('input',()=>{let v=cep.value.replace(/\D/g,'').slice(0,8);cep.value=v.length>5?v.slice(0,5)+'-'+v.slice(5):v});
  // Confirmacao ao remover item
  document.querySelectorAll('.remover').forEach(a=>a.addEventListener('click',e=>{if(!confirm('Remover este item?'))e.preventDefault()}));
});
