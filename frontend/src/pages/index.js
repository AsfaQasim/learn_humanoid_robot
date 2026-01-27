import React, { useState, Component } from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';
import Spline from '@splinetool/react-spline';

// Error Boundary Component for Spline
class SplineWithErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Spline component error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      // Fallback UI when Spline fails to load
      return (
        <div style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: '#f0f0f0',
          color: '#666',
          fontSize: '16px',
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '48px', marginBottom: '20px' }}>🤖</div>
            <p>3D Model Loading...</p>
            <p style={{ fontSize: '14px', marginTop: '10px' }}>(Check network connection)</p>
          </div>
        </div>
      );
    }

    return <Spline {...this.props} />;
  }
}

//  loader
const RobotLoader = () => (
  <div style={{
    position: 'absolute',
    top: 0,
    right: 0,
    width: '100%',
    height: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 10,
    pointerEvents: 'none',
    backgroundColor: 'rgba(255, 255, 255, 0)',
  }}>
    <div style={{
      width: '70px',
      height: '70px',
      borderRadius: '50%',
      border: '3px solid rgba(59,130,246,0.25)',
      borderTopColor: '#64748b',
      animation: 'spin 1.1s linear infinite',
    }} />
    <style>{`
      @keyframes spin {
        to { transform: rotate(360deg); }
      }
    `}</style>
  </div>
);

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  const [loading, setLoading] = useState(true);

  return (
    <Layout title={siteConfig.title}>
      {/* Hero Section */}
      <div style={{
        position: 'relative',
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
        overflow: 'hidden',
      }}>
        {/* Robot - ensuring interactivity and correct mobile layout */}
        <main className="robot-main-container" style={{
          position: 'absolute',
          top: 0,
          right: 0,
          width: '60%',
          height: '100%',
          zIndex: 1,
        }}>
          {loading && <RobotLoader />}
          <SplineWithErrorBoundary
            scene="https://prod.spline.design/Q5uh6cPZMc0R5C17/scene.splinecode"
            onLoad={() => setLoading(false)}
          />
        </main>

        {/* Left Text & Buttons */}
        <main style={{
          position: 'relative',
          zIndex: 2,
          padding: '4rem 2rem',
          maxWidth: '650px',
          marginLeft: '5%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          height: '100%',
        }}>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'flex-start',
            justifyContent: 'center',
            height: '100%',
          }}>
            <div style={{
              marginBottom: '2rem',
              padding: '0.5rem 1rem',
              background: 'linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.1) 100%)',
              borderRadius: '50px',
              border: '1px solid rgba(59, 130, 246, 0.2)',
              fontSize: '0.9rem',
              fontWeight: 600,
              color: '#3b82f6',
              display: 'inline-block',
            }}>
              Future of Robotics
            </div>
            <h1 style={{
              fontSize: 'clamp(2.5rem, 7vw, 4.5rem)',
              fontWeight: 800,
              lineHeight: 1.05,
              color: '#0f172a',
              margin: '0 0 1.5rem',
              letterSpacing: '-0.03em',
              maxWidth: '100%',
            }}>
              Physical AI & Humanoid Robotics
            </h1>
            <p style={{
              fontSize: 'clamp(1.1rem, 2.5vw, 1.25rem)',
              fontWeight: 400,
              lineHeight: 1.7,
              color: '#64748b',
              margin: '0 0 2.5rem 0',
              letterSpacing: '0.01em',
              maxWidth: '90%',
            }}>
              Bridging gap between digital intelligence and physical reality
            </p>
            <div style={{
              display: 'flex',
              gap: '1.25rem',
              flexWrap: 'wrap',
              marginTop: '1rem',
            }}>
              <a href="/docs/intro" className={`${styles.button} ${styles['button--lg']} ${styles['button--primary']}`} style={{
                padding: '1rem 2rem',
                fontSize: '1rem',
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
              }}>
                Get Started
              </a>
              <a href="/docs/robotics-module-one/index" className={`${styles.button} ${styles['button--lg']} ${styles['button--secondary']}`} style={{
                padding: '1rem 2rem',
                fontSize: '1rem',
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
              }}>
                View Curriculum
              </a>
            </div>
          </div>
        </main>

        <style>{`
          @media (max-width: 996px) {
            div[style*="height: '100vh'"] {
              height: auto !important;
              flex-direction: column !important;
              padding: 5rem 1rem 2rem 1rem !important;
            }
            .robot-main-container {
              position: relative !important;
              width: 100% !important;
              height: 350px !important;
              z-index: 10 !important;
              pointer-events: auto !important;
              margin-top: 2rem;
            }
            main[style*="maxWidth: '650px'"] {
              margin-left: 0 !important;
              padding: 2rem 1rem !important;
              text-align: center !important;
              max-width: 100% !important;
              z-index: 1 !important;
            }
            div[style*="display: 'flex'"][style*="gap: '1.25rem'"] {
              justify-content: center !important;
              width: 100%;
              flex-direction: column !important;
              align-items: center !important;
            }
            div[style*="display: 'flex'"][style*="gap: '1.25rem'"] a {
              width: 100% !important;
              max-width: 300px !important;
              text-align: center !important;
            }
          }
          @media (max-width: 480px) {
            h1 { font-size: 2.2rem !important; }
            .robot-main-container { height: 280px !important; }
            p { font-size: 1.1rem !important; }
            div[style*="display: 'flex'"][style*="gap: '1.25rem'"] {
              flex-direction: column !important;
              align-items: stretch !important;
              gap: 1rem !important;
            }
            div[style*="display: 'flex'"][style*="gap: '1.25rem'"] a {
              width: 100% !important;
              max-width: none !important;
              text-align: center !important;
            }
          }
        `}</style>
      </div>

      {/* Feature Section with Clean Grid UI */}
      <section style={{
        position: 'relative',
        zIndex: 1,
        padding: '8rem 2rem',
        background: 'linear-gradient(to bottom, #f8fafc 0%, #ffffff 100%)',
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>

          {/* Header */}
          <div style={{ textAlign: 'center', marginBottom: '5rem' }}>
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

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '2rem',
            marginBottom: '3rem',
          }} className="feature-grid-3">
            {/* Card 1 */}
            <div style={{
              padding: '2.5rem',
              borderRadius: '20px',
              background: 'linear-gradient(0deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.95) 100%)',
              border: '1px solid rgba(226, 232, 240, 0.6)',
              transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
              position: 'relative',
              overflow: 'hidden',
              boxShadow: '0 6px 24px rgba(0, 0, 0, 0.06)',
            }}
            onMouseEnter={(e) => {
              const topBar = e.currentTarget.querySelector('.feature-card-top-bar');
              if (topBar) topBar.style.opacity = '1';
              e.currentTarget.style.transform = 'translateY(-8px)';
              e.currentTarget.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.12)';
              e.currentTarget.style.borderColor = 'rgba(203, 213, 225, 0.8)';
            }}
            onMouseLeave={(e) => {
              const topBar = e.currentTarget.querySelector('.feature-card-top-bar');
              if (topBar) topBar.style.opacity = '0';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 6px 24px rgba(0, 0, 0, 0.06)';
              e.currentTarget.style.borderColor = 'rgba(226, 232, 240, 0.6)';
            }}>
              <div className="feature-card-top-bar" style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '4px',
                background: 'linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)',
                opacity: 0,
                transition: 'opacity 0.4s ease',
              }}></div>
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
                <svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '28px', height: '28px' }}>
                  <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                  <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                </svg>
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#0f172a', margin: '0 0 0.75rem', letterSpacing: '-0.01em' }}>Comprehensive Content</h3>
              <p style={{ fontSize: '0.95rem', lineHeight: 1.75, color: '#64748b', margin: '0' }}>
                Complete 13-week course covering Physical AI, ROS 2, Digital Twins, NVIDIA Isaac, Humanoid Development, and Conversational Robotics.
              </p>
            </div>

            {/* Card 2 */}
            <div style={{
              padding: '2.5rem',
              borderRadius: '20px',
              background: 'linear-gradient(0deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.95) 100%)',
              border: '1px solid rgba(226, 232, 240, 0.6)',
              transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
              position: 'relative',
              overflow: 'hidden',
              boxShadow: '0 6px 24px rgba(0, 0, 0, 0.06)',
            }}
            onMouseEnter={(e) => {
              const topBar = e.currentTarget.querySelector('.feature-card-top-bar');
              if (topBar) topBar.style.opacity = '1';
              e.currentTarget.style.transform = 'translateY(-8px)';
              e.currentTarget.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.12)';
              e.currentTarget.style.borderColor = 'rgba(203, 213, 225, 0.8)';
            }}
            onMouseLeave={(e) => {
              const topBar = e.currentTarget.querySelector('.feature-card-top-bar');
              if (topBar) topBar.style.opacity = '0';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 6px 24px rgba(0, 0, 0, 0.06)';
              e.currentTarget.style.borderColor = 'rgba(226, 232, 240, 0.6)';
            }}>
              <div className="feature-card-top-bar" style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '4px',
                background: 'linear-gradient(90deg, #8b5cf6 0%, #7c3aed 100%)',
                opacity: 0,
                transition: 'opacity 0.4s ease',
              }}></div>
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
                <svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '28px', height: '28px' }}>
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M8 12h8"/>
                  <path d="M12 8v8"/>
                </svg>
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#0f172a', margin: '0 0 0.75rem', letterSpacing: '-0.01em' }}>Interactive Chatbot</h3>
              <p style={{ fontSize: '0.95rem', lineHeight: 1.75, color: '#64748b', margin: '0' }}>
                Ask questions about textbook content with our RAG-powered chatbot. Get answers with citations, or ask about specific selected text.
              </p>
            </div>

            {/* Card 3 */}
            <div style={{
              padding: '2.5rem',
              borderRadius: '20px',
              background: 'linear-gradient(0deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.95) 100%)',
              border: '1px solid rgba(226, 232, 240, 0.6)',
              transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
              position: 'relative',
              overflow: 'hidden',
              boxShadow: '0 6px 24px rgba(0, 0, 0, 0.06)',
            }}
            onMouseEnter={(e) => {
              const topBar = e.currentTarget.querySelector('.feature-card-top-bar');
              if (topBar) topBar.style.opacity = '1';
              e.currentTarget.style.transform = 'translateY(-8px)';
              e.currentTarget.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.12)';
              e.currentTarget.style.borderColor = 'rgba(203, 213, 225, 0.8)';
            }}
            onMouseLeave={(e) => {
              const topBar = e.currentTarget.querySelector('.feature-card-top-bar');
              if (topBar) topBar.style.opacity = '0';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 6px 24px rgba(0, 0, 0, 0.06)';
              e.currentTarget.style.borderColor = 'rgba(226, 232, 240, 0.6)';
            }}>
              <div className="feature-card-top-bar" style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '4px',
                background: 'linear-gradient(90deg, #10b981 0%, #059669 100%)',
                opacity: 0,
                transition: 'opacity 0.4s ease',
              }}></div>
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
                <svg viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ width: '28px', height: '28px' }}>
                  <path d="M2 22v-6.5A3.5 3.5 0 0 1 5.5 12h5A3.5 3.5 0 0 1 14 15.5V22"/>
                  <circle cx="8" cy="4" r="3"/>
                  <path d="M16 22v-6.5A3.5 3.5 0 0 1 19.5 12h0a3.5 3.5 0 0 1 3.5 3.5V22"/>
                  <circle cx="20" cy="4" r="3"/>
                </svg>
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#0f172a', margin: '0 0 0.75rem', letterSpacing: '-0.01em' }}>Hands-On Labs</h3>
              <p style={{ fontSize: '0.95rem', lineHeight: 1.75, color: '#64748b', margin: '0' }}>
                Each chapter includes practical labs, exercises, and checkpoint quizzes to reinforce your learning through active practice.
              </p>
            </div>
          </div>

          {/* Row 2: 2 Cards */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(2, 1fr)',
            gap: '1.75rem',
          }} className="feature-grid-2">
            {/* Learning Path Card */}
            <div style={{
              padding: '2.5rem',
              borderRadius: '20px',
              background: 'linear-gradient(0deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.95) 100%)',
              border: '1px solid rgba(226, 232, 240, 0.6)',
              transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
              position: 'relative',
              overflow: 'hidden',
              boxShadow: '0 6px 24px rgba(0, 0, 0, 0.06)',
            }}>
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '4px',
                background: 'linear-gradient(90deg, #f59e0b 0%, #d97706 100%)',
                opacity: 1,
              }}></div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#0f172a', margin: '0 0 1.5rem', letterSpacing: '-0.01em' }}>Learning Path</h3>
              <ul style={{ margin: '0', paddingLeft: '0', listStyle: 'none' }}>
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
              padding: '2.5rem',
              borderRadius: '20px',
              background: 'linear-gradient(0deg, rgba(255,255,255,1) 0%, rgba(255,255,255,0.95) 100%)',
              border: '1px solid rgba(226, 232, 240, 0.6)',
              transition: 'all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275)',
              position: 'relative',
              overflow: 'hidden',
              boxShadow: '0 6px 24px rgba(0, 0, 0, 0.06)',
            }}>
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                height: '4px',
                background: 'linear-gradient(90deg, #ef4444 0%, #dc2626 100%)',
                opacity: 1,
              }}></div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: '#0f172a', margin: '0 0 1.5rem', letterSpacing: '-0.01em' }}>Quick Start</h3>
              <ol style={{ margin: '0', paddingLeft: '0', listStyle: 'none' }}>
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
            .feature-grid-3 {
              grid-template-columns: repeat(2, 1fr) !important;
            }
          }
          @media (max-width: 768px) {
            .feature-grid-3,
            .feature-grid-2 {
              grid-template-columns: 1fr !important;
              gap: 1.5rem !important;
            }
            section {
              padding: 4rem 1.5rem !important;
            }
            .feature-grid-3 > div,
            .feature-grid-2 > div {
              padding: 2rem !important;
            }
          }
          @media (max-width: 480px) {
            .feature-grid-3,
            .feature-grid-2 {
              gap: 1.25rem !important;
            }
            .feature-grid-3 > div,
            .feature-grid-2 > div {
              padding: 1.75rem !important;
            }
          }
        `}</style>
      </section>
    </Layout>
  );
}