// Minimal JS to handle form submissions via fetch and provide dynamic updates.
document.addEventListener('DOMContentLoaded', function(){
  // toast helper
  function showToast(message, type='info'){
    const container = document.getElementById('toastContainer');
    if(!container) return;
    const toastId = 't'+Date.now();
    const color = type === 'success' ? 'bg-success text-white' : (type==='error' ? 'bg-danger text-white' : 'bg-primary text-white');
    const html = `<div id="${toastId}" class="toast ${color}" role="alert" aria-live="assertive" aria-atomic="true"><div class="d-flex"><div class="toast-body">${message}</div><button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button></div></div>`;
    container.insertAdjacentHTML('beforeend', html);
    const el = document.getElementById(toastId);
    const bs = new bootstrap.Toast(el, {delay:4000});
    bs.show();
    // remove after hidden
    el.addEventListener('hidden.bs.toast', ()=> el.remove());
  }

  // Add student
  const addStudentForm = document.getElementById('addStudentForm');
  if(addStudentForm){
    addStudentForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const fd = new FormData(addStudentForm);
      const data = Object.fromEntries(fd.entries());
      const res = await fetch('/api/students', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
      if(res.ok){
        const js = await res.json();
        // append row to table
        const tbody = document.getElementById('studentsTable');
        const tr = document.createElement('tr');
        tr.setAttribute('data-id', js.id);
        tr.innerHTML = `<td class="col-id">${js.id}</td><td class="col-name">${escapeHtml(data.name)}</td><td class="col-email">${escapeHtml(data.email||'')}</td><td class="col-phone">${escapeHtml(data.phone||'')}</td><td class="col-branch">${escapeHtml(data.branch||'')}</td><td><button class="btn btn-sm btn-icon btn-outline-secondary btn-edit" title="Edit"><i class="fa-solid fa-pen-to-square"></i></button> <button class="btn btn-sm btn-icon btn-outline-danger btn-delete" title="Delete"><i class="fa-solid fa-trash"></i></button></td>`;
        tbody.prepend(tr);
        // reset form
        addStudentForm.reset();
        const modal = bootstrap.Modal.getInstance(document.getElementById('addStudentModal'));
        modal.hide();
        showToast('Student added','success');
      } else {
        const err = await res.json().catch(()=>({message:'Request failed'}));
        showToast(err.message||'Failed to add student','error');
      }
    });
  }

  // Edit / Delete students via event delegation
  const studentsTable = document.getElementById('studentsTable');
  if(studentsTable){
    studentsTable.addEventListener('click', async (e)=>{
      const tr = e.target.closest('tr');
      if(!tr) return;
      const id = tr.getAttribute('data-id');
      if(e.target.closest('.btn-edit')){
        // open edit modal and prefill
        const modalEl = document.getElementById('editStudentModal');
        const modal = new bootstrap.Modal(modalEl);
        modalEl.querySelector('input[name="id"]').value = id;
        modalEl.querySelector('input[name="name"]').value = tr.querySelector('.col-name').textContent.trim();
        modalEl.querySelector('input[name="email"]').value = tr.querySelector('.col-email').textContent.trim();
        modalEl.querySelector('input[name="phone"]').value = tr.querySelector('.col-phone').textContent.trim();
        modalEl.querySelector('input[name="branch"]').value = tr.querySelector('.col-branch').textContent.trim();
        modal.show();
      }
      if(e.target.closest('.btn-delete')){
        if(!confirm('Delete this student?')) return;
        const res = await fetch(`/api/students/${id}`, {method:'DELETE'});
        if(res.ok){ tr.remove(); showToast('Student deleted','success'); } else { const err = await res.json().catch(()=>({message:'Delete failed'})); showToast(err.message||'Delete failed','error'); }
      }
    });
  }

  // Handle update student
  const editStudentForm = document.getElementById('editStudentForm');
  if(editStudentForm){
    editStudentForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const fd = new FormData(editStudentForm);
      const data = Object.fromEntries(fd.entries());
      const id = data.id;
      const res = await fetch(`/api/students/${id}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
      if(res.ok){
        // update row DOM
        const tr = document.querySelector(`#studentsTable tr[data-id="${id}"]`);
        if(tr){
          tr.querySelector('.col-name').textContent = data.name;
          tr.querySelector('.col-email').textContent = data.email || '';
          tr.querySelector('.col-phone').textContent = data.phone || '';
          tr.querySelector('.col-branch').textContent = data.branch || '';
        }
        const modal = bootstrap.Modal.getInstance(document.getElementById('editStudentModal'));
        modal.hide();
        showToast('Student updated','success');
      } else { const err = await res.json().catch(()=>({message:'Update failed'})); showToast(err.message||'Update failed','error'); }
    });
  }

  const addCompanyForm = document.getElementById('addCompanyForm');
  if(addCompanyForm){
    addCompanyForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const fd = new FormData(addCompanyForm);
      const data = Object.fromEntries(fd.entries());
      const res = await fetch('/api/companies', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
      if(res.ok){
        const js = await res.json();
        const tbody = document.getElementById('companiesTable');
        const tr = document.createElement('tr');
        tr.setAttribute('data-id', js.id);
        tr.innerHTML = `<td class="col-id">${js.id}</td><td class="col-name">${escapeHtml(data.name)}</td><td class="col-contact">${escapeHtml(data.contact_person||'')}</td><td class="col-email">${escapeHtml(data.email||'')}</td><td class="col-phone">${escapeHtml(data.phone||'')}</td><td><button class="btn btn-sm btn-icon btn-outline-secondary btn-edit" title="Edit"><i class="fa-solid fa-pen-to-square"></i></button> <button class="btn btn-sm btn-icon btn-outline-danger btn-delete" title="Delete"><i class="fa-solid fa-trash"></i></button></td>`;
        tbody.prepend(tr);
        addCompanyForm.reset();
        const modal = bootstrap.Modal.getInstance(document.getElementById('addCompanyModal'));
        modal.hide();
        showToast('Company added','success');
      } else { const err = await res.json().catch(()=>({message:'Failed'})); showToast(err.message||'Failed to add company','error'); }
    });
  }

  const companiesTable = document.getElementById('companiesTable');
  if(companiesTable){
    companiesTable.addEventListener('click', async (e)=>{
      const tr = e.target.closest('tr'); if(!tr) return;
      const id = tr.getAttribute('data-id');
      if(e.target.closest('.btn-edit')){
        const modalEl = document.getElementById('editCompanyModal');
        const modal = new bootstrap.Modal(modalEl);
        modalEl.querySelector('input[name="id"]').value = id;
        modalEl.querySelector('input[name="name"]').value = tr.querySelector('.col-name').textContent.trim();
        modalEl.querySelector('input[name="contact_person"]').value = tr.querySelector('.col-contact').textContent.trim();
        modalEl.querySelector('input[name="email"]').value = tr.querySelector('.col-email').textContent.trim();
        modalEl.querySelector('input[name="phone"]').value = tr.querySelector('.col-phone').textContent.trim();
        modal.show();
      }
      if(e.target.closest('.btn-delete')){
        if(!confirm('Delete this company?')) return;
        const res = await fetch(`/api/companies/${id}`, {method:'DELETE'});
        if(res.ok){ tr.remove(); showToast('Company deleted','success'); } else { const err = await res.json().catch(()=>({message:'Delete failed'})); showToast(err.message||'Delete failed','error'); }
      }
    });
  }

  const editCompanyForm = document.getElementById('editCompanyForm');
  if(editCompanyForm){
    editCompanyForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const fd = new FormData(editCompanyForm);
      const data = Object.fromEntries(fd.entries());
      const id = data.id;
      const res = await fetch(`/api/companies/${id}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
      if(res.ok){
        const tr = document.querySelector(`#companiesTable tr[data-id="${id}"]`);
        if(tr){
          tr.querySelector('.col-name').textContent = data.name;
          tr.querySelector('.col-contact').textContent = data.contact_person || '';
          tr.querySelector('.col-email').textContent = data.email || '';
          tr.querySelector('.col-phone').textContent = data.phone || '';
        }
        const modal = bootstrap.Modal.getInstance(document.getElementById('editCompanyModal'));
        modal.hide();
        showToast('Company updated','success');
      } else { const err = await res.json().catch(()=>({message:'Update failed'})); showToast(err.message||'Update failed','error'); }
    });
  }

  const addInternForm = document.getElementById('addInternForm');
  if(addInternForm){
    addInternForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const fd = new FormData(addInternForm);
      const data = Object.fromEntries(fd.entries());
      const res = await fetch('/api/internships', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
      if(res.ok){
        const js = await res.json();
        const tbody = document.getElementById('internshipsTable');
        // get company name from select
        const select = addInternForm.querySelector('select[name="company_id"]');
        const companyName = select.options[select.selectedIndex].text;
        const tr = document.createElement('tr');
        tr.setAttribute('data-id', js.id);
        tr.innerHTML = `<td class="col-id">${js.id}</td><td class="col-title">${escapeHtml(data.title)}</td><td class="col-company" data-company-id="${data.company_id}">${escapeHtml(companyName)}</td><td class="col-dates">${escapeHtml(data.start_date||'')} - ${escapeHtml(data.end_date||'')}</td><td class="col-stipend">${escapeHtml(data.stipend||'')}</td><td class="col-seats">${escapeHtml(data.seats||'1')}</td><td><button class="btn btn-sm btn-icon btn-outline-secondary btn-edit" title="Edit"><i class="fa-solid fa-pen-to-square"></i></button> <button class="btn btn-sm btn-icon btn-outline-danger btn-delete" title="Delete"><i class="fa-solid fa-trash"></i></button></td>`;
        tbody.prepend(tr);
        addInternForm.reset();
        const modal = bootstrap.Modal.getInstance(document.getElementById('addInternModal'));
        modal.hide();
        showToast('Internship added','success');
      } else { const err = await res.json().catch(()=>({message:'Failed'})); showToast(err.message||'Failed to add internship','error'); }
    });
  }

  const internshipsTable = document.getElementById('internshipsTable');
  if(internshipsTable){
    internshipsTable.addEventListener('click', async (e)=>{
      const tr = e.target.closest('tr'); if(!tr) return;
      const id = tr.getAttribute('data-id');
      if(e.target.closest('.btn-edit')){
        const modalEl = document.getElementById('editInternModal');
        const modal = new bootstrap.Modal(modalEl);
        modalEl.querySelector('input[name="id"]').value = id;
        modalEl.querySelector('input[name="title"]').value = tr.querySelector('.col-title').textContent.trim();
        const companySelect = modalEl.querySelector('select[name="company_id"]');
        const companyId = tr.querySelector('.col-company').getAttribute('data-company-id');
        if(companyId){ companySelect.value = companyId; }
        const dates = tr.querySelector('.col-dates').textContent.split('-').map(s=>s.trim());
        modalEl.querySelector('input[name="start_date"]').value = dates[0]||'';
        modalEl.querySelector('input[name="end_date"]').value = dates[1]||'';
        modalEl.querySelector('input[name="stipend"]').value = tr.querySelector('.col-stipend').textContent.trim();
        modalEl.querySelector('input[name="seats"]').value = tr.querySelector('.col-seats').textContent.trim();
        modalEl.querySelector('textarea[name="description"]').value = '';
        modal.show();
      }
      if(e.target.closest('.btn-delete')){
        if(!confirm('Delete this internship?')) return;
        const res = await fetch(`/api/internships/${id}`, {method:'DELETE'});
        if(res.ok){ tr.remove(); showToast('Internship deleted','success'); } else { const err = await res.json().catch(()=>({message:'Delete failed'})); showToast(err.message||'Delete failed','error'); }
      }
    });
  }

  const editInternForm = document.getElementById('editInternForm');
  if(editInternForm){
    editInternForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const fd = new FormData(editInternForm);
      const data = Object.fromEntries(fd.entries());
      const id = data.id;
      const res = await fetch(`/api/internships/${id}`, {method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
      if(res.ok){
        const tr = document.querySelector(`#internshipsTable tr[data-id="${id}"]`);
        if(tr){
          tr.querySelector('.col-title').textContent = data.title;
          const selectedText = editInternForm.querySelector('select[name="company_id"]').selectedOptions[0].textContent;
          tr.querySelector('.col-company').textContent = selectedText;
          tr.querySelector('.col-company').setAttribute('data-company-id', data.company_id);
          tr.querySelector('.col-dates').textContent = `${data.start_date||''} - ${data.end_date||''}`;
          tr.querySelector('.col-stipend').textContent = data.stipend||'';
          tr.querySelector('.col-seats').textContent = data.seats||'';
        }
        const modal = bootstrap.Modal.getInstance(document.getElementById('editInternModal'));
        modal.hide();
        showToast('Internship updated','success');
      } else { const err = await res.json().catch(()=>({message:'Update failed'})); showToast(err.message||'Update failed','error'); }
    });
  }

  const addAppForm = document.getElementById('addAppForm');
  if(addAppForm){
    addAppForm.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const fd = new FormData(addAppForm);
      const data = Object.fromEntries(fd.entries());
      const res = await fetch('/api/applications', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
      if(res.ok){
        const js = await res.json();
        const tbody = document.getElementById('applicationsTable');
        const studentText = addAppForm.querySelector('select[name="student_id"]').selectedOptions[0].textContent;
        const internText = addAppForm.querySelector('select[name="internship_id"]').selectedOptions[0].textContent;
        const tr = document.createElement('tr');
        tr.setAttribute('data-id', js.id);
        tr.innerHTML = `<td class="col-id">${js.id}</td><td class="col-student">${escapeHtml(studentText)}</td><td class="col-internship">${escapeHtml(internText)}</td><td class="col-status">Applied</td><td class="col-applied">just now</td><td><button class="btn btn-sm btn-icon btn-outline-secondary btn-edit" title="Update"><i class="fa-solid fa-pen-to-square"></i></button> <button class="btn btn-sm btn-icon btn-outline-danger btn-delete" title="Delete"><i class="fa-solid fa-trash"></i></button></td>`;
        tbody.prepend(tr);
        addAppForm.reset();
        const modal = bootstrap.Modal.getInstance(document.getElementById('addAppModal'));
        modal.hide();
        showToast('Application submitted','success');
      } else { const err = await res.json().catch(()=>({message:'Failed'})); showToast(err.message||'Failed to submit application','error'); }
    });
  }

  const applicationsTable = document.getElementById('applicationsTable');
  if(applicationsTable){
    applicationsTable.addEventListener('click', async (e)=>{
      const tr = e.target.closest('tr'); 
      if(!tr) return;
      const id = tr.getAttribute('data-id');
      
      if(e.target.closest('.btn-view')){
        // Populate and show details modal
        const student = tr.querySelector('.col-student div div:first-child').textContent.trim();
        const email = tr.querySelector('.col-student div div:last-child').textContent.trim();
        const position = tr.querySelector('td:nth-child(2)').textContent.trim();
        const company = tr.querySelector('.col-company').textContent.trim();
        const applied = tr.querySelector('.col-applied').textContent.trim();
        const status = tr.querySelector('.status-badge').textContent.trim();
        
        document.getElementById('modal-student').textContent = student;
        document.getElementById('modal-email').textContent = email;
        document.getElementById('modal-position').textContent = position;
        document.getElementById('modal-company').textContent = company;
        document.getElementById('modal-date').textContent = applied;
        
        // Update status badge with correct color
        const statusBadge = document.getElementById('modal-status');
        statusBadge.textContent = status;
        statusBadge.className = `status-badge px-2.5 py-1 rounded-full text-sm font-medium ${getStatusColor(status)}`;
        
        // Set current status in dropdown
        document.getElementById('modal-status-update').value = status;
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('appDetailsModal'));
        
        // Handle status update
        const updateBtn = document.getElementById('update-status');
        updateBtn.onclick = async function(){
          const newStatus = document.getElementById('modal-status-update').value;
          const res = await fetch(`/api/applications/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({status: newStatus})
          });
          
          if(res.ok){
            // Update status badge in table and modal
            const badge = tr.querySelector('.status-badge');
            const modalBadge = document.getElementById('modal-status');
            const statusClass = getStatusColor(newStatus);
            
            badge.textContent = newStatus;
            badge.className = `status-badge px-2.5 py-1 rounded-full text-sm font-medium ${statusClass}`;
            modalBadge.textContent = newStatus;
            modalBadge.className = `status-badge px-2.5 py-1 rounded-full text-sm font-medium ${statusClass}`;
            
            showToast('Application status updated', 'success');
            modal.hide();
          } else {
            const err = await res.json().catch(() => ({message:'Update failed'}));
            showToast(err.message || 'Failed to update status', 'error');
          }
        };
        
        // Handle resume download
        const downloadBtn = document.getElementById('download-resume');
        downloadBtn.onclick = function(){
          showToast('Resume download not implemented in demo', 'info');
        };
        
        modal.show();
      }
      
      if(e.target.closest('.btn-delete')){
        if(!confirm('Delete this application?')) return;
        const res = await fetch(`/api/applications/${id}`, {method: 'DELETE'});
        if(res.ok){
          tr.remove();
          showToast('Application deleted', 'success');
          filterApplications(); // Update counter
        } else {
          const err = await res.json().catch(() => ({message: 'Delete failed'}));
          showToast(err.message || 'Failed to delete application', 'error');
        }
      }
    });
  }

  // Client-side filtering for applications
  const appSearch = document.getElementById('appSearch');
  const appFilter = document.getElementById('appFilter');
  function getStatusColor(status) {
    switch (status) {
      case 'Accepted':
        return 'bg-green-100 text-green-800';
      case 'Interview Scheduled':
        return 'bg-blue-100 text-blue-800';
      case 'Under Review':
        return 'bg-yellow-100 text-yellow-800';
      case 'Rejected':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }

  function filterApplications(){
    const q = (appSearch && appSearch.value || '').toLowerCase();
    const status = (appFilter && appFilter.value) || 'all';
    const rows = document.querySelectorAll('#applicationsTable tr');
    let shown = 0;
    rows.forEach(r=>{
      const student = (r.querySelector('.col-student') && r.querySelector('.col-student').textContent||'').toLowerCase();
      const internship = (r.querySelector('.col-internship') && r.querySelector('.col-internship').textContent||'').toLowerCase();
      const company = (r.querySelector('.col-company') && r.querySelector('.col-company').textContent||'').toLowerCase();
      const st = r.querySelector('.status-badge') ? r.querySelector('.status-badge').textContent.trim() : '';
      const matchesSearch = !q || student.includes(q) || internship.includes(q) || company.includes(q);
      const matchesStatus = status === 'all' || st === status;
      if(matchesSearch && matchesStatus){ r.style.display = ''; shown++; } else { r.style.display = 'none'; }
    });
    // Update counter
    const info = document.getElementById('applicationsInfo');
    if(info) info.textContent = `Showing ${shown} of ${rows.length} applications`;
  }
  if(appSearch) appSearch.addEventListener('input', filterApplications);
  if(appFilter) appFilter.addEventListener('change', filterApplications);
});

// utility to escape HTML when inserting user values
function escapeHtml(unsafe){
  if(typeof unsafe !== 'string') return unsafe;
  return unsafe.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;').replaceAll("'","&#039;");
}

