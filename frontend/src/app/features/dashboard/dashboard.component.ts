import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/services/auth.service';
import { AiService } from '../../core/services/ai.service';
import { ArchiveService, ArchivedCase } from '../../core/services/archive.service';

interface CaseItem {
  ref: string;
  title: string;
  client: string;
  category: string;
  lawyer: string;
  status: string;
  statusClass: string;
}

interface AgendaItem {
  day: string;
  month: string;
  title: string;
  location: string;
  time: string;
  desc: string;
  status: string;
}

interface ChatMessage {
  user: string;
  reply: string;
}

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  activeTab = 'dashboard';
  userEmail = '';
  userRole = '';

  // AI Widget State
  aiPrompt = '';
  aiOutput = '';
  isGeneratingAI = false;

  // AI Chat State
  chatInput = '';
  chatMessages: ChatMessage[] = [];

  // Smart Archiving State
  archivedCases: ArchivedCase[] = [];
  searchQuery = '';
  isSemanticSearch = false;
  selectedCategory = '';
  selectedOutcome = '';
  isSearchingArchives = false;

  // Demo Data
  recentCases: CaseItem[] = [
    { ref: '2026-DK-01', title: 'Litige Foncier Almadies', client: 'El Hadj Gueye', category: 'Civil', lawyer: 'Me. Diallo', status: 'En cours', statusClass: 'bg-warning' },
    { ref: '2026-DK-02', title: 'Recouvrement créance SENELEC', client: 'SOMACO SARL', category: 'Commercial', lawyer: 'Me. Diallo', status: 'Gagné', statusClass: 'bg-success' },
    { ref: '2026-DK-03', title: 'Contestation licenciement', client: 'Fatou Ndiaye', category: 'Social', lawyer: 'Me. Sow', status: 'En cours', statusClass: 'bg-warning' }
  ];

  allCases: CaseItem[] = [];

  agendaItems: AgendaItem[] = [
    { day: '04', month: 'Juil', title: 'Audience de plaidoirie - Litige Gueye', location: 'Tribunal de Grande Instance de Dakar', time: '09h00', desc: 'Présentation des conclusions récapitulatives et des pièces justificatives.', status: 'À venir' },
    { day: '08', month: 'Juil', title: 'Rendez-vous client - Signature protocole', location: 'Cabinet Diallo', time: '15h00', desc: 'Finalisation du protocole d\'accord transactionnel avec la SOMACO.', status: 'À venir' },
    { day: '12', month: 'Juil', title: 'Délibéré - Affaire Contestation Sociale', location: 'Tribunal du Travail de Dakar', time: '10h00', desc: 'Lecture de la décision du tribunal concernant le licenciement de Fatou Ndiaye.', status: 'À venir' }
  ];

  constructor(
    private authService: AuthService, 
    private aiService: AiService,
    private archiveService: ArchiveService,
    private router: Router
  ) {}

  ngOnInit() {
    if (!this.authService.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }
    this.userEmail = this.authService.getUserEmail() || 'avocat@cabinet.com';
    this.userRole = (this.authService.getUserRole() || 'AVOCAT').toUpperCase();
    this.allCases = [...this.recentCases];

    // Mettre un onglet par défaut accessible pour chaque rôle
    if (this.userRole === 'COMPTABLE') {
      this.activeTab = 'billing';
    } else {
      this.activeTab = 'dashboard';
    }

    this.loadArchives();
  }

  hasAccess(tab: string): boolean {
    const role = this.userRole;
    if (role === 'AVOCAT' || role === 'ASSOCIATE') {
      return true; // L'avocat a accès à tout
    }
    if (role === 'SECRETAIRE') {
      return ['dashboard', 'cases', 'calendar', 'archives'].includes(tab);
    }
    if (role === 'COMPTABLE') {
      return ['dashboard', 'billing'].includes(tab);
    }
    return false;
  }


  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  generateAI() {
    if (!this.aiPrompt) return;
    this.isGeneratingAI = true;
    this.aiOutput = '';

    this.aiService.generateDocument(this.aiPrompt, 'mise_en_demeure').subscribe({
      next: (res) => {
        this.aiOutput = res.document_content;
        this.isGeneratingAI = false;
      },
      error: (err) => {
        console.error(err);
        this.aiOutput = 'Erreur lors de la génération de l\'acte via le serveur.';
        this.isGeneratingAI = false;
      }
    });
  }

  sendChatMessage() {
    if (!this.chatInput) return;
    const userQuery = this.chatInput;
    this.chatInput = '';

    this.aiService.askAI(userQuery).subscribe({
      next: (res) => {
        this.chatMessages.push({
          user: userQuery,
          reply: res.reply
        });
      },
      error: (err) => {
        console.error(err);
        this.chatMessages.push({
          user: userQuery,
          reply: 'Une erreur de communication avec le serveur IA est survenue.'
        });
      }
    });
  }

  addSampleCase() {
    const nextId = this.allCases.length + 1;
    const newCase: CaseItem = {
      ref: `2026-DK-0${nextId}`,
      title: `Affaire Contentieuse N°${nextId}`,
      client: 'Nouveau Client SARL',
      category: 'Commercial',
      lawyer: 'Me. Diallo',
      status: 'En cours',
      statusClass: 'bg-warning'
    };
    this.allCases.push(newCase);
  }

  loadArchives() {
    this.archiveService.getAllArchives().subscribe({
      next: (res) => {
        this.archivedCases = res;
      },
      error: (err) => {
        console.error('Erreur lors du chargement des archives:', err);
      }
    });
  }

  searchArchives() {
    this.isSearchingArchives = true;
    this.archiveService.searchArchives({
      query: this.searchQuery,
      semantic: this.isSemanticSearch,
      category: this.selectedCategory || undefined,
      outcome: this.selectedOutcome || undefined
    }).subscribe({
      next: (res) => {
        this.archivedCases = res;
        this.isSearchingArchives = false;
      },
      error: (err) => {
        console.error('Erreur lors de la recherche dans les archives:', err);
        this.isSearchingArchives = false;
      }
    });
  }

  inspireFromCase(caseItem: ArchivedCase) {
    this.chatInput = `Je prépare un dossier similaire à l'affaire "${caseItem.title}". Peux-tu me rédiger un projet d'acte en t'inspirant des arguments clés utilisés à l'époque : "${caseItem.key_arguments}" ?`;
    this.activeTab = 'ia';
  }
}
