import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatResponse {
  reply: string;
  is_mocked: boolean;
  details?: string;
}

export interface DocumentResponse {
  document_content: string;
  is_mocked: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class AiService {
  private apiUrl = 'http://localhost:8000/api/v1/ia';

  constructor(private http: HttpClient) {}

  askAI(query: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(`${this.apiUrl}/chat`, { query });
  }

  generateDocument(prompt: string, docType: string): Observable<DocumentResponse> {
    return this.http.post<DocumentResponse>(`${this.apiUrl}/generate-document`, {
      prompt,
      doc_type: docType
    });
  }
}
