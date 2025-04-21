import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Output, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { DocumentsService } from '../../services/documents.service';
import { HttpClientModule, provideHttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-bulletin',
  standalone: true,
  imports: [CommonModule, FormsModule], // Remove HttpClientModule from here
  templateUrl: './bulletin.component.html',
  styleUrls: ['./bulletin.component.css'],
})


export class BulletinComponent implements OnInit {
  formData = {
    prenom: '',
    nom: '',
    adresse: '',
    codePostal: '',
    prenomMalade: '',
    nomMalade: '',
    assureSocial: false,
    conjoint: false,
    enfant: false,
    ascendant: false,
    dateNaissance: '',
    numTel: '',
    refDossier: '',
    identifiantUnique: '',
    cnss: false,
    cnrps: false,
    convbi: false,
    patientType: 'self'
  };
  

  originalFormData: any = {};
  identifiant: string[] = Array(12).fill('');
  originalIdentifiant: string[] = Array(12).fill('');
  isEditMode: boolean = false;
  showStatusAlert: boolean = false;
  
  files: { name: string; id: string }[] = [];
  selectedIndex = 0;

  @Output() formSubmit = new EventEmitter<any>();
  @Output() dataVerified = new EventEmitter<any>();

constructor(
  private documentsService: DocumentsService,
  private router: Router
) {
  const state = this.router.getCurrentNavigation()?.extras.state as any;
  this.files = state?.files || [];
}


  ngOnInit(): void {
    this.loadDataFromDatabase();
  }

  loadDataFromDatabase(): void {
    this.documentsService.getBulletinData().subscribe({
      next: (data) => {
        if (data) {
          this.formData = { ...data };
          
          const idString = data.identifiantUnique || '';
          for (let i = 0; i < 12; i++) {
            this.identifiant[i] = idString[i] || '';
          }
          
          this.saveOriginalState();
        }
      },
      error: (err) => {
        console.error('Error loading data:', err);
        // Fallback to default data if needed
        this.loadDefaultData();
      }
    });
  }
  
  // Add this method to handle the fallback case
  loadDefaultData(): void {
    const extractedData = {
      prenom: 'Mohammed',
      nom: 'Ben Ali',
      adresse: '15 Rue de Tunis',
      codePostal: '1002',
      prenomMalade: 'Mohammed',
      nomMalade: 'Ben Ali',
      dateNaissance: '12/05/1980',
      numTel: '98765432',
      refDossier: 'REF-2025-04-123',
      cnss: true,
      cnrps: false,
      convbi: false,
      assureSocial: true,
      conjoint: false,
      enfant: false,
      ascendant: false,
      patientType: 'self',
      identifiantUnique: '12131343'
    };
  
    this.formData = { ...extractedData };
  
    const idString = extractedData.identifiantUnique || '';
    for (let i = 0; i < 12; i++) {
      this.identifiant[i] = idString[i] || '';
    }
  
    this.saveOriginalState();
  }

  saveOriginalState(): void {
    this.originalFormData = JSON.parse(JSON.stringify(this.formData));
    this.originalIdentifiant = [...this.identifiant];
  }

  toggleEditMode(): void {
    if (this.isEditMode) {
      this.saveChanges();
    } else {
      this.isEditMode = true;
      this.showStatusAlert = true;
    }
  }

  saveChanges(): void {
    this.isEditMode = false;
    this.showStatusAlert = true;

    this.saveOriginalState();
    this.dataVerified.emit(this.getCompleteFormData());

    setTimeout(() => {
      this.showStatusAlert = false;
    }, 3000);
  }


  onSubmit(): void {
    const data = this.getCompleteFormData();

    this.documentsService.saveBulletinData(data).subscribe({
      next: (res) => {
        console.log('Success:', res);
        alert('Document submitted successfully!');
      },
      error: (err) => {
        console.error('Error submitting document:', err);
        alert('Failed to submit document.');
      }
    });
  }

  getCompleteFormData(): any {
    const identifiantValue = this.identifiant.join('');
    return {
      ...this.formData,
      identifiant: identifiantValue
    };
  }

  setPatientType(type: string): void {
    if (!this.isEditMode) return; // Prevent changes if not in edit mode
  
    // Reset all malade options
    this.formData.assureSocial = false;
    this.formData.conjoint = false;
    this.formData.enfant = false;
    this.formData.ascendant = false;
  
    // Set the selected option
    switch (type) {
      case 'assureSocial':
        this.formData.assureSocial = true;
        break;
      case 'conjoint':
        this.formData.conjoint = true;
        break;
      case 'enfant':
        this.formData.enfant = true;
        break;
      case 'ascendant':
        this.formData.ascendant = true;
        break;
    }
  }

  resetForm(): void {
    this.formData = {
      prenom: '',
      nom: '',
      adresse: '',
      codePostal: '',
      prenomMalade: '',
      nomMalade: '',
      dateNaissance: '',
      numTel: '',
      refDossier: '',
      identifiantUnique: '',
      assureSocial: false,
      conjoint: false,
      enfant: false,
      ascendant: false,
      cnss: false,
      cnrps: false,
      convbi: false,
      patientType: 'self'
    };
    this.identifiant = Array(12).fill('');
    this.saveOriginalState();
  }

  onCheckboxChange(checkboxName: string): void {
    if (checkboxName === 'cnss' && this.formData.cnss) {
      this.formData.cnrps = false;
      this.formData.convbi = false;
    } else if (checkboxName === 'cnrps' && this.formData.cnrps) {
      this.formData.cnss = false;
      this.formData.convbi = false;
    } else if (checkboxName === 'convbi' && this.formData.convbi) {
      this.formData.cnss = false;
      this.formData.cnrps = false;
    }
  }
}
