import * as Dialog from '@radix-ui/react-dialog';

export default function JobDialog({ open, onOpenChange, job, onChange, onSave }) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="dialog-overlay" />
        <Dialog.Content className="dialog-content" aria-describedby="job-dialog-desc">
          <Dialog.Title>{job.id ? 'Edit Job' : 'Add Job'}</Dialog.Title>
          <Dialog.Description id="job-dialog-desc">
            {job.id ? 'Edit the job details below.' : 'Fill in the details to add a new job.'}
          </Dialog.Description>
          <form
            onSubmit={e => {
              e.preventDefault();
              onSave();
            }}
          >
            <input
              value={job.title || ''}
              onChange={e => onChange({ ...job, title: e.target.value })}
              placeholder="Job Title"
              required
            />
            <input
              value={job.company || ''}
              onChange={e => onChange({ ...job, company: e.target.value })}
              placeholder="Company"
              required
            />
            {/* Add more fields as needed */}
            <button type="submit">{job.id ? 'Update' : 'Add'}</button>
          </form>
          <Dialog.Close asChild>
            <button>Close</button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
} 