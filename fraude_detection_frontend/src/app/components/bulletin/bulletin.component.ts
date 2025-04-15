import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

interface UploadFile {
  file: File;
  documentType: string;
  id: string;
}

@Component({
  selector: 'app-bulletin',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './bulletin.component.html',
  styleUrls: ['./bulletin.component.css']
})
export class BulletinComponent {
  bulletinId = '123'; // Replace with dynamic value if needed
  prescriptionId = '456'; // Replace with dynamic value if needed
  
  // Flags to check document existence
  isBulletinUploaded = false;
  isPrescriptionUploaded = false;

  constructor(private router: Router) { }

  goToBulletin() {
    this.router.navigate(['/bulletin', this.bulletinId]);
  }
  
  goToPrescription() {
    this.router.navigate(['/prescription', this.prescriptionId]);
  }

  // Check if both documents are uploaded
  checkDocuments() {
    if (!this.isBulletinUploaded) {
      // Show "File Not Found" message and upload UI for "Bulletin de Soin"
      this.showFileNotFound('Bulletin de Soin');
    } else if (!this.isPrescriptionUploaded) {
      // Show "File Not Found" message and upload UI for "Ordonnance"
      this.showFileNotFound('Ordonnance');
    } else {
      // Proceed with showing the actual content
      this.showContent();
    }
  }

  // Display "File Not Found" message with upload form
  showFileNotFound(documentType: string) {
    // Display message and show upload UI for the missing document
    console.log(`${documentType} not found. Please upload the file.`);
    // Example of setting up the upload UI (this could be part of the HTML)
    this.uploadDocument(documentType);
  }

  // Show content if both documents are uploaded
  showContent() {
    console.log('Both documents are uploaded. Show content here.');
  }

  // Handle document upload logic
  uploadDocument(documentType: string) {
    console.log(`Preparing to upload ${documentType}`);
    // You can integrate this part with an actual file upload component/UI
  }




 @Output() close = new EventEmitter<boolean>();
  
  // Changed from single documentType to uploadFiles with individual types
  uploadFiles: UploadFile[] = [];
  isUploading = false;
  uploadProgress = 0;
  

  // Constants
  readonly MAX_FILES = 3;
  readonly ALLOWED_TYPES = ['image/jpeg', 'image/png', 'application/pdf'];
  readonly documentTypes = [
    { value: 'ordonnance', label: 'Ordonnance' },
    { value: 'bulletin', label: 'Bulletin de Soins' },
    { value: 'cnam', label: 'Carte CNAM' }
  ];
  
  get canAddMoreFiles(): boolean {
    return this.uploadFiles.length < this.MAX_FILES;
  }
  
  get isSubmitDisabled(): boolean {
    // Check if we have files and all files have a document type
    return this.uploadFiles.length === 0 || 
           this.uploadFiles.some(file => !file.documentType) || 
           this.isUploading;
  }
  
  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    if (this.canAddMoreFiles) {
      const dropArea = document.getElementById('drop-area');
      if (dropArea) dropArea.classList.add('active');
    }
  }
  
  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    const dropArea = document.getElementById('drop-area');
    if (dropArea) dropArea.classList.remove('active');
  }
  
  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    const dropArea = document.getElementById('drop-area');
    if (dropArea) dropArea.classList.remove('active');
    
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
      event.target.value = ''; // Reset input
      return;
    }
    
    const files = event.target.files;
    if (files) {
      this.handleFiles(files);
    }
    event.target.value = ''; // Reset input for future selections
  }
  
  handleFiles(files: FileList): void {
    const remainingSlots = this.MAX_FILES - this.uploadFiles.length;
    const filesToAdd = Math.min(files.length, remainingSlots);
    
    for (let i = 0; i < filesToAdd; i++) {
      const file = files[i];
      
      // Validate file type if needed
      if (this.ALLOWED_TYPES.includes(file.type)) {
        // Create a new UploadFile with an empty document type initially
        this.uploadFiles.push({
          file: file,
          documentType: '',
          id: this.generateUniqueId()
        });
      } else {
        this.showError(`File type not supported: ${file.name}`);
      }
    }
    
    if (files.length > remainingSlots) {
      this.showError(`Only added ${filesToAdd} files. Maximum limit of ${this.MAX_FILES} reached.`);
    }
  }
  
  removeFile(index: number): void {
    this.uploadFiles.splice(index, 1);
  }
  
  showError(message: string): void {
    // You can implement a proper error notification system
    // For now, just using alert
    alert(message);
  }
  
  closeModal(): void {
    this.close.emit(false);
  }
  
  generateUniqueId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substring(2);
  }
  
  uploadDocuments(): void {
    if (this.uploadFiles.length === 0) {
      this.showError('Please select at least one file');
      return;
    }
    
    // Check if all files have document types selected
    const missingTypeFiles = this.uploadFiles.filter(file => !file.documentType);
    if (missingTypeFiles.length > 0) {
      this.showError('Please select document type for all files');
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
  
  processExtractedDocuments(): void {
    // Close modal first
    this.close.emit(true);
    
    // Group files by document type
    const ordonnanceFiles = this.uploadFiles.filter(file => file.documentType === 'ordonnance');
    const bulletinFiles = this.uploadFiles.filter(file => file.documentType === 'bulletin');
    const cnamFiles = this.uploadFiles.filter(file => file.documentType === 'cnam');
    
    // Process in order: ordonnance, bulletin, cnam
    // Navigate to the first non-empty group
    if (ordonnanceFiles.length > 0) {
      // In a real app, you'd generate a real document ID from your backend
      const documentId = this.generateUniqueId();
      this.router.navigate([`prescription/${documentId}`]);
    } else if (bulletinFiles.length > 0) {
      const documentId = this.generateUniqueId();
      this.router.navigate([`bulletin/${documentId}`]);
    } else if (cnamFiles.length > 0) {
      const documentId = this.generateUniqueId();
      this.router.navigate([`cnam-card/${documentId}`]);
    } else {
      this.router.navigate(['/dashboard']);
    }
    
    // Note: In a real application, you would save all files to the server first,
    // then navigate to the appropriate view with the document IDs returned from the server
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
    if (size < 1024) {
      return `${size} B`;
    } else if (size < 1024 * 1024) {
      return `${(size / 1024).toFixed(1)} KB`;
    } else {
      return `${(size / (1024 * 1024)).toFixed(1)} MB`;
    }
  }

}
