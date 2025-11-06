import React, { useMemo, useState } from 'react';

export default function Applications({ applications = [] }) {
  const [filterStatus, setFilterStatus] = useState('all');
  const [query, setQuery] = useState('');

  const filteredApps = useMemo(() => {
    const q = (query || '').trim().toLowerCase();
    return applications.filter((app) => {
      if (filterStatus !== 'all') {
        const appStatus = (app.status || '').toLowerCase();
        if (appStatus !== filterStatus.toLowerCase()) {
          return false;
        }
      }
      if (!q) return true;
      
      const fields = [
        app.student_name,
        app.internship_title || app.title || '',
        app.company_name,
        app.student_email,
        app.status,
      ];
      return fields.some((f) => (f || '').toString().toLowerCase().includes(q));
    });
  }, [applications, filterStatus, query]);

  const formatDate = (d) => {
    if (!d) return '—';
    try {
      const dt = new Date(d);
      return dt.toLocaleDateString(undefined, { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
      });
    } catch {
      return d.toString();
    }
  };

  const getStatusClass = (status) => {
    const baseClasses = "inline-block px-3 py-1 rounded-full text-xs font-medium";
    switch (status?.toLowerCase()) {
      case 'applied':
      case 'pending':
        return `${baseClasses} bg-yellow-100 text-yellow-800`;
      case 'selected':
      case 'accepted':
        return `${baseClasses} bg-green-100 text-green-800`;
      case 'rejected':
        return `${baseClasses} bg-red-100 text-red-800`;
      case 'under review':
        return `${baseClasses} bg-blue-100 text-blue-800`;
      default:
        return `${baseClasses} bg-gray-100 text-gray-800`;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="relative">
            <label className="sr-only" htmlFor="status">Filter by Status</label>
            <select
              id="status"
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="w-48 appearance-none bg-white border border-gray-200 px-4 py-2 pr-8 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            >
              <option value="all">All Statuses</option>
              <option value="applied">Applied</option>
              <option value="pending">Pending</option>
              <option value="under review">Under Review</option>
              <option value="selected">Selected</option>
              <option value="rejected">Rejected</option>
            </select>
            <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none">
              <svg className="h-4 w-4 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </div>
          </div>

          <div className="relative flex-1 min-w-[300px]">
            <input
              type="search"
              id="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search applications..."
              className="w-full px-4 py-2 pr-10 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            />
            <div className="absolute right-3 top-1/2 -translate-y-1/2">
              <svg className="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
        </div>

        <div className="text-sm text-gray-500">
          Showing <span className="font-medium text-gray-900">{filteredApps.length}</span> of{' '}
          <span className="font-medium text-gray-900">{applications.length}</span> applications
        </div>
      </div>

      <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full w-full table-auto">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Student
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Position
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Company
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Applied Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredApps.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-8 text-center text-sm text-gray-500">
                    No applications found
                  </td>
                </tr>
              ) : (
                filteredApps.map((app) => (
                  <tr 
                    key={app.id || `${app.student_email}-${app.internship_id}`}
                    className="hover:bg-gray-50 transition-colors"
                  >
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex flex-col">
                        <div className="text-sm font-medium text-gray-900">
                          {app.student_name || '—'}
                        </div>
                        {app.student_email && (
                          <div className="text-sm text-gray-500">
                            {app.student_email}
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {app.internship_title || app.title || '—'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {app.company_name || '—'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {formatDate(app.applied_at || app.applied_at_date || app.created_at)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={getStatusClass(app.status)}>
                        {app.status || 'Unknown'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right">
                      <div className="inline-flex items-center gap-2">
                        <button
                          type="button"
                          className="inline-flex items-center px-3 py-1.5 text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                        >
                          View
                        </button>
                        <button
                          type="button"
                          className="inline-flex items-center px-3 py-1.5 text-sm font-medium rounded-md text-gray-700 bg-gray-100 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                        >
                          Edit
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
