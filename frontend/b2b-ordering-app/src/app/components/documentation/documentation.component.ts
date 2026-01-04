import { Component } from '@angular/core';

@Component({
  selector: 'app-documentation',
  templateUrl: './documentation.component.html',
  styleUrls: ['./documentation.component.scss']
})
export class DocumentationComponent {
  // Informations du site
  siteName = 'B2B Ordering System';
  description = `This internal B2B ordering system allows employees of a company
  to manage products and orders efficiently.`;

  whyDeveloped = `Developed during the Christmas holidays 2025 to improve my skills
  in microservice architecture and full-stack development.`;

  useCase = `This system can be used in a company to streamline internal
  order management, product tracking, and departmental ordering workflows.`;

  githubLink = 'https://github.com/MicroservicesAPI/B2B-Odering-Management-System';
  authorName = 'Steve cabrel kamguia';
  linkedinLink = 'https://www.linkedin.com/in/steve-cabrel-kamguia-144989257/';
  portfolioLink = 'https://steve-kamguia.kascali.de/home';
}
