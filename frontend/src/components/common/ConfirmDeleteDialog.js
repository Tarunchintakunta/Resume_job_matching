import * as Dialog from '@radix-ui/react-dialog';

export default function ConfirmDeleteDialog({ open, onOpenChange, onConfirm, description }) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="dialog-overlay" />
        <Dialog.Content className="dialog-content" aria-describedby="delete-dialog-desc">
          <Dialog.Title>Delete?</Dialog.Title>
          <Dialog.Description id="delete-dialog-desc">
            {description || 'Are you sure you want to delete this item?'}
          </Dialog.Description>
          <button onClick={onConfirm}>Yes, Delete</button>
          <Dialog.Close asChild>
            <button>No, Cancel</button>
          </Dialog.Close>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
} 