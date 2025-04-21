import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { BulletinComponent } from './components/bulletin/bulletin.component';
import { PrescriptionComponent } from './components/prescription/prescription.component';
import { CnamCardComponent } from './components/cnam-card/cnam-card.component';
import { NgModule } from '@angular/core';
import { UploadComponent } from './components/upload/upload.component';
import { UploadDocComponent } from './components/upload-doc/upload-doc.component';

export const routes: Routes = [
    { path: '', component: UploadDocComponent },
    { path: 'extracted/:id', component: BulletinComponent },
    { path: 'prescription/:id', component: PrescriptionComponent },
    { path: 'upload', component: UploadComponent   },
    { path: 'cnam-card/:id', component: CnamCardComponent },
  ];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
  })
  export class AppRoutingModule {}