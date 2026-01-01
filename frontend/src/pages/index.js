import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import HeroRobot from '../components/HeroRobot/HeroRobot';

export default function Home() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout title={`${siteConfig.title}`}>
      {/* Hero Section - Full viewport height only */}
      <div style={{
        position: 'relative',
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        background: 'linear-gradient(135deg, #0a0c1e 0%, #0f1228 50%, #1a1f3a 100%)',
        overflow: 'hidden',
      }}>
        {/* Robot - Fixed in hero section only */}
        <main style={{
          position: 'absolute',
          top: 0,
          right: 0,
          width: '60%',
          height: '100%',
          zIndex: 1,
        }}>
          <HeroRobot />
        </main>

        {/* Text & Buttons - Left Side */}
        <main style={{
          position: 'relative',
          zIndex: 2,
          padding: '4rem 2rem',
          maxWidth: '650px',
          marginLeft: '5%',
        }}>
          <h1 style={{
            fontSize: 'clamp(2.5rem, 7vw, 4.5rem)',
            fontWeight: 700,
            lineHeight: 1.1,
            color: '#0f172a',
            margin: '0 0 1rem',
            letterSpacing: '-0.02em',
          }}>
            Physical AI & Humanoid Robotics
          </h1>
          <p style={{
            fontSize: 'clamp(1.1rem, 2.5vw, 1.25rem)',
            fontWeight: 400,
            lineHeight: 1.8,
            color: '#64748b',
            margin: '1.5rem 0 2.5rem 0',
            letterSpacing: '0.01em',
          }}>
            Bridging gap between digital intelligence and physical reality
          </p>
          <div style={{
            display: 'flex',
            gap: '0.875rem',
            flexWrap: 'wrap',
            marginTop: '0.5rem',
          }}>
            <a href="/docs/intro" style={{
              padding: '0.875rem 2rem',
              fontSize: '0.95rem',
              fontWeight: 600,
              backgroundColor: '#0f172a',
              color: '#ffffff',
              borderRadius: '8px',
              textDecoration: 'none',
              transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
              letterSpacing: '0.025em',
              textTransform: 'none',
            }}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = '#1e293b';
              e.target.style.transform = 'translateY(-2px)';
              e.target.style.boxShadow = '0 8px 24px rgba(15, 23, 42, 0.2)';
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = '#0f172a';
              e.target.style.transform = 'translateY(0)';
              e.target.style.boxShadow = 'none';
            }}>
              Get Started
            </a>
            <a href="/docs/robotics-module-one/index" style={{
              padding: '0.875rem 2rem',
              fontSize: '0.95rem',
              fontWeight: 600,
              backgroundColor: '#ffffff',
              color: '#0f172a',
              border: '1.5px solid #e2e8f0',
              borderRadius: '8px',
              textDecoration: 'none',
              transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
              letterSpacing: '0.025em',
              textTransform: 'none',
            }}
            onMouseEnter={(e) => {
              e.target.style.borderColor = '#0f172a';
              e.target.style.backgroundColor = '#f8fafc';
              e.target.style.transform = 'translateY(-2px)';
            }}
            onMouseLeave={(e) => {
              e.target.style.borderColor = '#e2e8f0';
              e.target.style.backgroundColor = '#ffffff';
              e.target.style.transform = 'translateY(0)';
            }}>
              View Curriculum
            </a>
          </div>
        </main>
      </div>

      {/* Feature Section */}
      <section style={{
        position: 'relative',
        zIndex: 1,
        padding: '8rem 2rem',
        background: 'linear-gradient(to bottom, #f8fafc 0%, #ffffff 100%)',
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
        }}>
          {/* Section Header */}
          <div style={{
            textAlign: 'center',
            marginBottom: '5rem',
          }}>
            <h2 style={{
              fontSize: 'clamp(2rem, 4vw, 2.5rem)',
              fontWeight: 700,
              color: '#0f172a',
              margin: '0 0 1rem',
              letterSpacing: '-0.01em',
            }}>
              What You'll Learn
            </h2>
            <p style={{
              fontSize: '1.125rem',
              color: '#64748b',
              maxWidth: '600px',
              margin: '0 auto',
              lineHeight: 1.7,
            }}>
              A comprehensive 13-week journey into future of robotics and AI
            </p>
          </div>

          {/* Row 1: 3 Feature Cards */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '1.75rem',
            marginBottom: '3rem',
          }}>
            {/* Card 1 */}
            <div style={{
              padding: '2.25rem',
              borderRadius: '12px',
              background: '#ffffff',
              border: '1px solid #e2e8f0',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.08)';
              e.currentTarget.style.borderColor = '#cbd5e1';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
              e.currentTarget.style.borderColor = '#e2e8f0';
            }}>
              <div style={{
                width: '56px',
                height: '56px',
                margin: '0 0 1.5rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                borderRadius: '12px',
                background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
              }}>
                <svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{
                  width: '28px',
                  height: '28px',
                }}>
                  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                  <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                </svg>
              </div>
              <h3 style={{
                fontSize: '1.25rem',
                fontWeight: 600,
                color: '#0f172a',
                margin: '0 0 0.75rem',
                letterSpacing: '-0.01em',
              }}>
                Comprehensive Content
              </h3>
              <p style={{
                fontSize: '0.95rem',
                lineHeight: 1.75,
                color: '#64748b',
                margin: '0',
              }}>
                Complete 13-week course covering Physical AI, ROS 2, Digital Twins, NVIDIA Isaac, Humanoid Development, and Conversational Robotics.
              </p>
            </div>

            {/* Card 2 */}
            <div style={{
              padding: '2.25rem',
              borderRadius: '12px',
              background: '#ffffff',
              border: '1px solid #e2e8f0',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.08)';
              e.currentTarget.style.borderColor = '#cbd5e1';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
              e.currentTarget.style.borderColor = '#e2e8f0';
            }}>
              <div style={{
                width: '56px',
                height: '56px',
                margin: '0 0 1.5rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                borderRadius: '12px',
                background: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)',
              }}>
                <svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{
                  width: '28px',
                  height: '28px',
                }}>
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M8 12h8"/>
                  <path d="M12 8v8"/>
                </svg>
              </div>
              <h3 style={{
                fontSize: '1.25rem',
                fontWeight: 600,
                color: '#0f172a',
                margin: '0 0 0.75rem',
                letterSpacing: '-0.01em',
              }}>
                Interactive Chatbot
              </h3>
              <p style={{
                fontSize: '0.95rem',
                lineHeight: 1.75,
                color: '#64748b',
                margin: '0',
              }}>
                Ask questions about textbook content with our RAG-powered chatbot. Get answers with citations, or ask about specific selected text.
              </p>
            </div>

            {/* Card 3 */}
            <div style={{
              padding: '2.25rem',
              borderRadius: '12px',
              background: '#ffffff',
              border: '1px solid #e2e8f0',
              transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.08)';
              e.currentTarget.style.borderColor = '#cbd5e1';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
              e.currentTarget.style.borderColor = '#e2e8f0';
            }}>
              <div style={{
                width: '56px',
                height: '56px',
                margin: '0 0 1.5rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                borderRadius: '12px',
                background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              }}>
                <svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{
                  width: '28px',
                  height: '28px',
                }}>
                  <path d="M2 22v-6.5A3.5 3.5 0 0 1 5.5 12h5A3.5 3.5 0 0 1 14 15.5V22"/>
                  <circle cx="8" cy="4" r="3"/>
                  <path d="M16 22v-6.5A3.5 3.5 0 0 1 19.5 12h0a3.5 3.5 0 0 1 3.5 3.5V22"/>
                  <circle cx="20" cy="4" r="3"/>
                </svg>
              </div>
              <h3 style={{
                fontSize: '1.25rem',
                fontWeight: 600,
                color: '#0f172a',
                margin: '0 0 0.75rem',
                letterSpacing: '-0.01em',
              }}>
                Hands-On Labs
              </h3>
              <p style={{
                fontSize: '0.95rem',
                lineHeight: 1.75,
                color: '#64748b',
                margin: '0',
              }}>
                Each chapter includes practical labs, exercises, and checkpoint quizzes to reinforce your learning through active practice.
              </p>
            </div>
          </div>

          {/* Row 2: 2 Cards */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(2, 1fr)',
            gap: '1.75rem',
          }}>
            {/* Learning Path Card */}
            <div style={{
              padding: '2.25rem',
              borderRadius: '12px',
              background: '#ffffff',
              border: '1px solid #e2e8f0',
            }}>
              <h3 style={{
                fontSize: '1.25rem',
                fontWeight: 600,
                color: '#0f172a',
                margin: '0 0 1.5rem',
                letterSpacing: '-0.01em',
              }}>
                Learning Path
              </h3>
              <ul style={{
                margin: '0',
                paddingLeft: '0',
                listStyle: 'none',
              }}>
                {[
                  'Foundations (Weeks 1-2)',
                  'ROS 2 Nervous System (Weeks 3-5)',
                  'Digital Twin (Weeks 6-7)'
                ].map((item, index) => (
                  <li key={index} style={{
                    padding: '0.875rem 0',
                    borderBottom: '1px solid #f1f5f9',
                    fontSize: '0.95rem',
                    color: '#475569',
                    lineHeight: 1.6,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                  }}>
                    <span style={{
                      width: '6px',
                      height: '6px',
                      borderRadius: '50%',
                      background: '#3b82f6',
                      flexShrink: 0,
                    }}></span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>

            {/* Quick Start Card */}
            <div style={{
              padding: '2.25rem',
              borderRadius: '12px',
              background: '#ffffff',
              border: '1px solid #e2e8f0',
            }}>
              <h3 style={{
                fontSize: '1.25rem',
                fontWeight: 600,
                color: '#0f172a',
                margin: '0 0 1.5rem',
                letterSpacing: '-0.01em',
              }}>
                Quick Start
              </h3>
              <ol style={{
                margin: '0',
                paddingLeft: '0',
                listStyle: 'none',
              }}>
                {[
                  'Read Preface to understand how to use this book',
                  'Check Hardware Tracks for setup requirements',
                  'Start with Foundations'
                ].map((item, index) => (
                  <li key={index} style={{
                    padding: '0.875rem 0',
                    borderBottom: '1px solid #f1f5f9',
                    fontSize: '0.95rem',
                    color: '#475569',
                    lineHeight: 1.6,
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '0.875rem',
                  }}>
                    <span style={{
                      width: '24px',
                      height: '24px',
                      borderRadius: '6px',
                      background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                      color: '#ffffff',
                      fontSize: '0.75rem',
                      fontWeight: 600,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0,
                      marginTop: '0.125rem',
                    }}>
                      {index + 1}
                    </span>
                    <span style={{ flex: 1 }}>{item}</span>
                  </li>
                ))}
              </ol>
            </div>
          </div>
        </div>

        {/* Mobile Responsive Styles */}
        <style>{`
          @media (max-width: 1024px) {
            section > div > div[style*="grid-template-columns: repeat(3, 1fr)"] {
              grid-template-columns: repeat(2, 1fr) !important;
            }
          }
          @media (max-width: 768px) {
            section > div > div[style*="grid-template-columns: repeat(3, 1fr)"],
            section > div > div[style*="grid-template-columns: repeat(2, 1fr)"] {
              grid-template-columns: 1fr !important;
            }
            section {
              padding: 4rem 1.5rem !important;
            }
          }
        `}</style>
      </section>
    </Layout>
  );
}
