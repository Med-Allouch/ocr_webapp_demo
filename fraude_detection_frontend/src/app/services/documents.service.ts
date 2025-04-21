// documents.service.ts
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DocumentsService {
  private apiUrl = 'http://localhost:8000'; // Your FastAPI base URL
  
  constructor(private http: HttpClient) {} 

  getBulletinData(id?: string): Observable<any> {
    // If an ID is provided, fetch specific bulletin, otherwise get the latest or default
    const url = id 
      ? `${this.apiUrl}/bulletin/${id}` 
      : `${this.apiUrl}/bulletin/latest`;
    
    return this.http.get(url);
  }

  saveBulletinData(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/bulletin`, data);
  }
}