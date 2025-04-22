import { RouterModule, Routes } from '@angular/router';
import { BulletinComponent } from './components/bulletin/bulletin.component';
import { NgModule } from '@angular/core';
import { UploadDocComponent } from './components/upload-doc/upload-doc.component';
export const routes: Routes = [
  { path: '', component: UploadDocComponent },
  { path: 'bulletin/:id', component: BulletinComponent },
  { path: 'extracted/:id', component: BulletinComponent },
  { path: 'extracted/tabs', component: BulletinComponent },
  { path: '', redirectTo: '/bulletin/latest', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }