import React, { useState } from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';
import Spline from '@splinetool/react-spline';
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
          <Spline
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
            <a href="/docs/intro" className={`${styles.button} ${styles['button--lg']} ${styles['button--primary']}`}>
              Get Started
            </a>
            <a href="/docs/robotics-module-one/index" className={`${styles.button} ${styles['button--lg']} ${styles['button--secondary']}`}>
              View Curriculum
            </a>
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
            div[style*="display: 'flex'"][style*="gap: '0.875rem'"] {
              justify-content: center !important;
              width: 100%;
            }
          }
          @media (max-width: 480px) {
            h1 { font-size: 2rem !important; }
            .robot-main-container { height: 280px !important; }
            div[style*="display: 'flex'"][style*="gap: '0.875rem'"] {
              flex-direction: column;
              align-items: stretch;
            }
            div[style*="display: 'flex'"][style*="gap: '0.875rem'"] a {
              width: 100%;
              text-align: center;
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
            gap: '1.75rem',
            marginBottom: '3rem',
          }} className="feature-grid-3">
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
              padding: '2.25rem',
              borderRadius: '12px',
              background: '#ffffff',
              border: '1px solid #e2e8f0',
            }}>
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
              padding: '2.25rem',
              borderRadius: '12px',
              background: '#ffffff',
              border: '1px solid #e2e8f0',
            }}>
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
