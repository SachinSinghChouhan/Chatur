import React from 'react';
import { Github, Twitter, Mail, Heart } from 'lucide-react';

export function Footer() {
  return (
    <footer
      className="py-12 px-6 border-t"
      style={{
        backgroundColor: 'var(--background-secondary)',
        borderColor: 'var(--surface-border)',
      }}
    >
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-8">
          {/* About */}
          <div>
            <h4 className="mb-4" style={{ color: 'var(--text-primary)' }}>
              About Chatur
            </h4>
            <p className="text-sm mb-4" style={{ color: 'var(--text-muted)' }}>
              An open-source bilingual voice assistant that respects your privacy. Built with care for the Indian Windows user.
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="mb-4" style={{ color: 'var(--text-primary)' }}>
              Quick Links
            </h4>
            <ul className="space-y-2">
              <li>
                <a
                  href="#"
                  className="text-sm hover:opacity-70 transition-opacity"
                  style={{ color: 'var(--text-secondary)' }}
                >
                  Documentation
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-sm hover:opacity-70 transition-opacity"
                  style={{ color: 'var(--text-secondary)' }}
                >
                  Contributing Guide
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-sm hover:opacity-70 transition-opacity"
                  style={{ color: 'var(--text-secondary)' }}
                >
                  Release Notes
                </a>
              </li>
              <li>
                <a
                  href="#"
                  className="text-sm hover:opacity-70 transition-opacity"
                  style={{ color: 'var(--text-secondary)' }}
                >
                  Privacy Policy
                </a>
              </li>
            </ul>
          </div>

          {/* Community */}
          <div>
            <h4 className="mb-4" style={{ color: 'var(--text-primary)' }}>
              Community
            </h4>
            <div className="flex gap-4 mb-4">
              <a
                href="#"
                className="hover:opacity-70 transition-opacity"
                aria-label="GitHub"
              >
                <Github className="w-5 h-5" style={{ color: 'var(--text-secondary)' }} />
              </a>
              <a
                href="#"
                className="hover:opacity-70 transition-opacity"
                aria-label="Twitter"
              >
                <Twitter className="w-5 h-5" style={{ color: 'var(--text-secondary)' }} />
              </a>
              <a
                href="#"
                className="hover:opacity-70 transition-opacity"
                aria-label="Email"
              >
                <Mail className="w-5 h-5" style={{ color: 'var(--text-secondary)' }} />
              </a>
            </div>
            <p className="text-sm" style={{ color: 'var(--text-muted)' }}>
              Join our community and help shape the future of Chatur.
            </p>
          </div>
        </div>

        {/* Bottom */}
        <div
          className="pt-8 border-t flex flex-col sm:flex-row justify-between items-center gap-4"
          style={{ borderColor: 'var(--surface-border)' }}
        >
          <p className="text-sm" style={{ color: 'var(--text-muted)' }}>
            © 2026 Chatur. Open source under MIT License.
          </p>
          <p className="text-sm flex items-center gap-1" style={{ color: 'var(--text-muted)' }}>
            Made with <Heart className="w-4 h-4" style={{ color: 'var(--accent-primary)' }} /> for the community
          </p>
        </div>
      </div>
    </footer>
  );
}