import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpEventType } from '@angular/common/http';
import { Observable, throwError, of } from 'rxjs';
import { catchError, tap, map, filter } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DocumentsService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  uploadDocuments(files: File[]): Observable<any> {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file)); // 'files' not 'files[]'
  
    return this.http.post(`${this.apiUrl}/bulletin/upload`, formData).pipe(
      tap(response => console.log('Upload success:', response)),
      catchError(this.handleError('Error uploading documents'))
    );
  }
  

  getBulletinById(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/bulletin/${id}`).pipe(
      catchError(this.handleError(`Error fetching bulletin with ID ${id}`))
    );
  }

  saveBulletinData(data: any): Observable<any> {
    if (data.id) {
      return this.http.put(`${this.apiUrl}/bulletin/${data.id}`, data).pipe(
        tap(savedData => console.log('Bulletin updated:', savedData)),
        catchError(this.handleError('Error updating bulletin'))
      );
    } else {
      return this.http.post(`${this.apiUrl}/bulletin/`, data).pipe(
        tap(savedData => console.log('New bulletin created:', savedData)),
        catchError(this.handleError('Error creating bulletin'))
      );
    }
  }

  getLatestBulletin(): Observable<any> {
    return this.http.get(`${this.apiUrl}/bulletin/uploaded/latest`).pipe(
      catchError(error => {
        console.error('Error fetching latest bulletin:', error);
        // Return a default value for any error, not just 404
        return of({ filename: null, original_name: null, uploaded_at: null, exists: false });
      })
    );
  }

  getAllUploadedBulletins(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/bulletin/uploaded/all`).pipe(
      catchError(error => {
        if (error.status === 404) {
          return of([]);
        }
        return throwError(() => error);
      })
    );
  }

  private handleError(message: string) {
    return (error: HttpErrorResponse) => {
      console.error(`${message}:`, error);
      return throwError(() => new Error(message));
    };
  }
}