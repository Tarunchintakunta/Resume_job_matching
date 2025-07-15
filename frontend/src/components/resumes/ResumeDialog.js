import * as Dialog from '@radix-ui/react-dialog';

export default function ResumeDialog({ open, onOpenChange, resume }) {
  if (!resume) return null;
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="dialog-overlay" />
        <Dialog.Content className="dialog-content" aria-describedby="resume-dialog-desc">
          <Dialog.Title>Resume Profile</Dialog.Title>
          <Dialog.Description id="resume-dialog-desc">
            View all details for this candidate.
          </Dialog.Description>
          <div style={{ margin: '1rem 0' }}>
            <strong>Name:</strong> {resume.name}<br />
            <strong>Email:</strong> {resume.email}<br />
            <strong>Phone:</strong> {resume.phone}<br />
            <strong>Summary:</strong> <div style={{ whiteSpace: 'pre-line', marginBottom: 8 }}>{resume.summary}</div>
            <strong>Skills:</strong> {resume.skills && resume.skills.length > 0 ? (
              <ul>{resume.skills.map((s, i) => <li key={i}>{s}</li>)}</ul>
            ) : 'None'}
            <strong>Education:</strong> {resume.education && resume.education.length > 0 ? (
              <ul>{resume.education.map((e, i) => <li key={i}>{JSON.stringify(e)}</li>)}</ul>
            ) : 'None'}
            <strong>Experience:</strong> {resume.experience && resume.experience.length > 0 ? (
              <ul>{resume.experience.map((e, i) => <li key={i}>{JSON.stringify(e)}</li>)}</ul>
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