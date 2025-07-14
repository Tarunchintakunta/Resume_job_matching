import * as Dialog from '@radix-ui/react-dialog';

export default function JobDialog({ open, onOpenChange, job }) {
  if (!job) return null;
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="dialog-overlay" />
        <Dialog.Content className="dialog-content" aria-describedby="job-dialog-desc">
          <Dialog.Title>Job Details</Dialog.Title>
          <Dialog.Description id="job-dialog-desc">
            View all details for this job posting.
          </Dialog.Description>
          <div style={{ margin: '1rem 0' }}>
            <strong>Title:</strong> {job.title}<br />
            <strong>Company:</strong> {job.company}<br />
            <strong>Description:</strong> <div style={{ whiteSpace: 'pre-line', marginBottom: 8 }}>{job.description}</div>
            <strong>Location:</strong> {job.location || 'N/A'}<br />
            <strong>Job Type:</strong> {job.job_type || 'N/A'}<br />
            <strong>Experience Required:</strong> {job.experience_required || 0} years<br />
            <strong>Salary Range:</strong> {job.salary_range || 'N/A'}<br />
            <strong>Skills Required:</strong> {job.skills_required && job.skills_required.length > 0 ? (
              <ul>{job.skills_required.map((s, i) => <li key={i}>{s}</li>)}</ul>
            ) : 'None'}
            <strong>Requirements:</strong> {job.requirements && job.requirements.length > 0 ? (
              <ul>{job.requirements.map((r, i) => <li key={i}>{r}</li>)}</ul>
            ) : 'None'}
            <strong>Qualifications:</strong> {job.qualifications && job.qualifications.length > 0 ? (
              <ul>{job.qualifications.map((q, i) => <li key={i}>{q}</li>)}</ul>
            ) : 'None'}
          </div>
          <Dialog.Close asChild>
            <button>Close</button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
} 