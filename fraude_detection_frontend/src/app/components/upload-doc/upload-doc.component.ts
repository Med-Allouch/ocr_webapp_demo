import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

interface UploadFile {
  file: File;
  id: string;
}

@Component({
  selector: 'app-upload-doc',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './upload-doc.component.html',
  styleUrl: './upload-doc.component.css'
})
export class UploadDocComponent {

  @Output() close = new EventEmitter<boolean>();

  uploadFiles: UploadFile[] = [];
  isUploading = false;
  uploadProgress = 0;

  readonly MAX_FILES = 5;
  readonly ALLOWED_TYPES = ['image/jpeg', 'image/png', 'application/pdf'];

  constructor(private router: Router) {}

  get canAddMoreFiles(): boolean {
    return this.uploadFiles.length < this.MAX_FILES;
  }

  get isSubmitDisabled(): boolean {
    return this.uploadFiles.length === 0 || this.isUploading;
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    if (this.canAddMoreFiles) {
      document.getElementById('drop-area')?.classList.add('active');
    }
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('drop-area')?.classList.remove('active');
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    document.getElementById('drop-area')?.classList.remove('active');

    if (!this.canAddMoreFiles) {
      this.showError(`Maximum ${this.MAX_FILES} files allowed`);
      return;
    }

    const files = event.dataTransfer?.files;
    if (files) {
      this.handleFiles(files);
    }
  }

  onFileSelected(event: any): void {
    if (!this.canAddMoreFiles) {
      this.showError(`Maximum ${this.MAX_FILES} files allowed`);
      event.target.value = '';
      return;
    }

    const files = event.target.files;
    if (files) {
      this.handleFiles(files);
    }

    event.target.value = '';
  }

  handleFiles(files: FileList): void {
    const remainingSlots = this.MAX_FILES - this.uploadFiles.length;
    const filesToAdd = Math.min(files.length, remainingSlots);

    for (let i = 0; i < filesToAdd; i++) {
      const file = files[i];

      if (this.ALLOWED_TYPES.includes(file.type)) {
        this.uploadFiles.push({
          file: file,
          id: this.generateUniqueId()
        });
      } else {
        this.showError(`Unsupported file type: ${file.name}`);
      }
    }

    if (files.length > remainingSlots) {
      this.showError(`Only added ${filesToAdd} file(s). Maximum of ${this.MAX_FILES} allowed.`);
    }
  }

  removeFile(index: number): void {
    this.uploadFiles.splice(index, 1);
  }

  showError(message: string): void {
    alert(message);
  }

  closeSection(): void {
    this.close.emit(false);
  }

  uploadDocuments(): void {
    if (this.uploadFiles.length === 0) {
      this.showError('Please select at least one file');
      return;
    }

    this.isUploading = true;
    let progress = 0;
    const interval = setInterval(() => {
      progress += 15;
      this.uploadProgress = progress;

      if (progress >= 100) {
        clearInterval(interval);
        setTimeout(() => {
          this.isUploading = false;
          this.processExtractedDocuments();
        }, 500);
      }
    }, 300);
  }

  goToDocument() {

    this.router.navigate(['/', 'bulletin/:id'])
    .then(nav => {
      console.log(nav); // true if navigation is successful
    }, err => {
      console.log(err) // when there's an error
    });

    }

    processExtractedDocuments(): void {
      this.close.emit(true);
    
      if (this.uploadFiles.length === 1) {
        // Create file info object
        const fileInfo = {
          name: this.uploadFiles[0].file.name,
          id: this.uploadFiles[0].id
        };
        
        // Navigate to single file view with state data
        this.router.navigate([`extracted/${fileInfo.id}`], {
          state: { files: [fileInfo] }
        });
      } else {
        this.router.navigate(['extracted/tabs'], {
          state: { 
            files: this.uploadFiles.map(file => ({
              name: file.file.name,
              id: file.id
            }))
          }
        });
      }
    }

  generateUniqueId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substring(2);
  }

  getFileIcon(file: File): string {
    if (file.type.includes('pdf')) {
      return 'pdf-icon';
    } else if (file.type.includes('image')) {
      return 'image-icon';
    } else {
      return 'file-icon';
    }
  }

  formatFileSize(size: number): string {
    if (size < 1024) return `${size} B`;
    if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
    return `${(size / (1024 * 1024)).toFixed(1)} MB`;
  }
}
