import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ArchivedCase {
  id: number;
  ref: string;
  title: string;
  client: string;
  category: string;
  summary: string;
  outcome: string;
  key_arguments: string;
  location: string;
  year: number;
}

export interface SearchRequest {
  query: string;
  semantic: boolean;
  category?: string;
  outcome?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ArchiveService {
  private apiUrl = 'http://localhost:8000/api/v1/archives';

  constructor(private http: HttpClient) {}

  getAllArchives(): Observable<ArchivedCase[]> {
    return this.http.get<ArchivedCase[]>(this.apiUrl);
  }

  searchArchives(params: SearchRequest): Observable<ArchivedCase[]> {
    return this.http.post<ArchivedCase[]>(`${this.apiUrl}/search`, params);
  }
}
