import React from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function About() {
  const { siteConfig } = useDocusaurusContext();

  return (
    <Layout title={`About - ${siteConfig.title}`}>
      {/* Hero Section */}
      <section style={{
        position: 'relative',
        minHeight: '35vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#ffffff',
      }}>
        <div style={{
          textAlign: 'center',
          padding: '3rem 2rem',
          maxWidth: '800px',
        }}>
          <h1 style={{
            fontSize: 'clamp(2.5rem, 5vw, 3rem)',
            fontWeight: 700,
            color: '#0f172a',
            margin: '0 0 0.75rem',
            letterSpacing: '-0.02em',
          }}>
            About
          </h1>
          <p style={{
            fontSize: '1.125rem',
            color: '#64748b',
            margin: '0',
            lineHeight: 1.6,
          }}>
            Physical AI & Humanoid Robotics Textbook
          </p>
        </div>
      </section>

      {/* Main Content */}
      <section style={{
        padding: '5rem 2rem',
        background: '#ffffff',
      }}>
        <div style={{
          maxWidth: '1100px',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '4rem',
        }}>

          {/* Left Column */}
          <div>
            {/* Mission Card */}
            <div style={{
              marginBottom: '3rem',
            }}>
              <h2 style={{
                fontSize: '1.5rem',
                fontWeight: 700,
                color: '#0f172a',
                margin: '0 0 1.5rem',
                letterSpacing: '-0.01em',
              }}>
                Our Mission
              </h2>
              <p style={{
                fontSize: '1rem',
                lineHeight: 1.8,
                color: '#475569',
                margin: '0',
              }}>
                The Physical AI & Humanoid Robotics Textbook provides comprehensive education in AI-powered robotics. We bridge the gap between theoretical knowledge and practical application, making advanced robotics concepts accessible to developers at all levels.
              </p>
            </div>

            {/* What You'll Find Card */}
            <div style={{
              marginBottom: '3rem',
            }}>
              <h2 style={{
                fontSize: '1.5rem',
                fontWeight: 700,
                color: '#0f172a',
                margin: '0 0 1.5rem',
                letterSpacing: '-0.01em',
              }}>
                What You'll Find
              </h2>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
                gap: '1.25rem',
                marginTop: '1.5rem',
              }}>
                {[
                  { title: 'Comprehensive Course', desc: '13-week curriculum covering Physical AI, ROS 2, Digital Twins, NVIDIA Isaac' },
                  { title: 'Interactive Learning', desc: 'RAG-powered chatbot with citations for real-time assistance' },
                  { title: 'Hands-On Labs', desc: 'Practical exercises and quizzes in every chapter' },
                  { title: 'Expert Resources', desc: 'Content designed by robotics and AI professionals' },
                ].map((item, index) => (
                  <div key={index} style={{
                    padding: '1.5rem',
                    borderRadius: '12px',
                    background: '#f8fafc',
                    border: '1px solid #e2e8f0',
                    transition: 'all 0.3s ease',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = '#cbd5e1';
                    e.currentTarget.style.transform = 'translateY(-2px)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = '#e2e8f0';
                    e.currentTarget.style.transform = 'translateY(0)';
                  }}>
                    <h3 style={{
                      fontSize: '1.125rem',
                      fontWeight: 600,
                      color: '#0f172a',
                      margin: '0 0 0.75rem',
                    }}>
                      {item.title}
                    </h3>
                    <p style={{
                      fontSize: '0.95rem',
                      lineHeight: 1.6,
                      color: '#64748b',
                      margin: '0',
                    }}>
                      {item.desc}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Technology Stack Card */}
            <div style={{
              marginBottom: '3rem',
            }}>
              <h2 style={{
                fontSize: '1.5rem',
                fontWeight: 700,
                color: '#0f172a',
                margin: '0 0 1.5rem',
                letterSpacing: '-0.01em',
              }}>
                Technology Stack
              </h2>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
                gap: '0.75rem',
                marginTop: '1.5rem',
              }}>
                {[
                  'React', 'Docusaurus', 'ROS 2', 'NVIDIA Isaac',
                  'Python', 'FastAPI', 'Cohere AI', 'Qdrant'
                ].map((tech) => (
                  <span key={tech} style={{
                    padding: '0.5rem 1rem',
                    borderRadius: '8px',
                    background: '#ffffff',
                    border: '1px solid #e2e8f0',
                    fontSize: '0.875rem',
                    fontWeight: 500,
                    color: '#475569',
                    textAlign: 'center',
                    display: 'inline-block',
                  }}>
                    {tech}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column - Profile */}
          <div>
            {/* Profile Card */}
            <div style={{
              marginBottom: '3rem',
            }}>
              <h2 style={{
                fontSize: '1.5rem',
                fontWeight: 700,
                color: '#0f172a',
                margin: '0 0 1.5rem',
                letterSpacing: '-0.01em',
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
              }}>
                <span style={{
                  display: 'inline-flex',
                  width: '40px',
                  height: '40px',
                  borderRadius: '10px',
                  background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '1.125rem',
                  fontWeight: 600,
                  color: '#ffffff',
                }}>
                  AQ
                </span>
                Developer Profile
              </h2>

              <div style={{
                padding: '2rem',
                borderRadius: '12px',
                background: '#f8fafc',
                border: '1px solid #e2e8f0',
              }}>
                {/* Name */}
                <div style={{
                  marginBottom: '1.5rem',
                }}>
                  <h3 style={{
                    fontSize: '1.125rem',
                    fontWeight: 600,
                    color: '#0f172a',
                    margin: '0 0 0.5rem',
                  }}>
                    Asfa Qasim
                  </h3>
                  <p style={{
                    fontSize: '0.9rem',
                    lineHeight: 1.6,
                    color: '#64748b',
                    margin: '0',
                  }}>
                    Full Stack Developer & AI Enthusiast
                  </p>
                </div>

                {/* Bio */}
                <div style={{
                  marginBottom: '1.5rem',
                }}>
                  <p style={{
                    fontSize: '0.95rem',
                    lineHeight: 1.7,
                    color: '#475569',
                    margin: '0',
                  }}>
                    Passionate about building innovative solutions at the intersection of artificial intelligence and physical robotics. Currently focused on creating comprehensive educational resources that make advanced robotics concepts accessible to everyone.
                  </p>
                </div>

                {/* Skills */}
                <div style={{
                  marginBottom: '1.5rem',
                }}>
                  <h4 style={{
                    fontSize: '0.9rem',
                    fontWeight: 600,
                    color: '#0f172a',
                    margin: '0 0 0.75rem',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                  }}>
                    Skills & Expertise
                  </h4>
                  <div style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '0.5rem',
                    marginTop: '0.75rem',
                  }}>
                    {[
                      'Physical AI', 'ROS 2', 'Humanoid Robotics', 'Digital Twins',
                      'NVIDIA Isaac', 'RAG Systems', 'Full Stack Dev'
                    ].map((skill) => (
                      <span key={skill} style={{
                        padding: '0.4rem 0.8rem',
                        borderRadius: '6px',
                        background: '#ffffff',
                        border: '1px solid #e2e8f0',
                        fontSize: '0.8rem',
                        fontWeight: 500,
                        color: '#475569',
                      }}>
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* GitHub Button */}
                <a
                  href="https://github.com/AsfaQasim?tab=repositories"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    padding: '0.875rem 1.5rem',
                    borderRadius: '8px',
                    background: '#0f172a',
                    color: '#ffffff',
                    fontSize: '0.9rem',
                    fontWeight: 600,
                    textDecoration: 'none',
                    transition: 'all 0.25s ease',
                    width: '100%',
                    justifyContent: 'center',
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.background = '#1e293b';
                    e.target.style.transform = 'translateY(-2px)';
                    e.target.style.boxShadow = '0 4px 12px rgba(15, 23, 42, 0.15)';
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.background = '#0f172a';
                    e.target.style.transform = 'translateY(0)';
                    e.target.style.boxShadow = 'none';
                  }}
                >
                  <svg viewBox="0 0 24 24" fill="currentColor" style={{
                    width: '20px',
                    height: '20px',
                  }}>
                    <path d="M12 0c-6.626 0-12 5.373-12 12v24c0 6.626 5.373 12 12 12 0 6.626-5.373 12-12v-24c0-6.626-5.373-12-12zm0 16l-6-6v-4l6-6v-4z"/>
                  </svg>
                  <span>View GitHub Profile</span>
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Section */}
        <div style={{
          background: '#f8fafc',
          padding: '4rem 2rem',
        }}>
          <div style={{
            maxWidth: '1000px',
            margin: '0 auto',
            textAlign: 'center',
          }}>
            <h3 style={{
              fontSize: '1.125rem',
              fontWeight: 600,
              color: '#0f172a',
              marginBottom: '2rem',
              letterSpacing: '-0.01em',
            }}>
              Project Highlights
            </h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '2.5rem',
            }}>
              {[
                { number: '13+', label: 'Weeks of Content', color: '#3b82f6' },
                { number: '5+', label: 'Core Modules', color: '#8b5cf6' },
                { number: '50+', label: 'Practical Labs', color: '#10b981' },
                { number: '24/7', label: 'Support Available', color: '#f59e0b' },
              ].map((stat, index) => (
                <div key={index} style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: '0.75rem',
                }}>
                  <div style={{
                    fontSize: '3.5rem',
                    fontWeight: 700,
                    background: `linear-gradient(135deg, ${stat.color} 0%, ${stat.color} 100%)`,
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                    color: 'transparent',
                  }}>
                    {stat.number}
                  </div>
                  <span style={{
                    fontSize: '0.95rem',
                    color: '#64748b',
                    textAlign: 'center',
                  }}>
                    {stat.label}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Mobile Responsive Styles */}
        <style>{`
          @media (max-width: 1024px) {
            section:nth-of-type(2) > div {
              grid-template-columns: 1fr !important;
              gap: 3rem !important;
            }
          }
          @media (max-width: 768px) {
            section {
              padding: 3rem 1.5rem !important;
            }
            section:nth-of-type(1) {
              minHeight: 25vh !important;
            }
            section:nth-of-type(2) > div {
              gap: 2rem !important;
            }
            h1 {
              font-size: 2rem !important;
            }
            h2 {
              font-size: 1.25rem !important;
            }
          }
        `}</style>
      </section>
    </Layout>
  );
}
