import React from 'react';
import clsx from 'clsx';
import { HeroRobot } from '../HeroRobot';
import styles from './HomepageHero.module.css';

/**
 * HomepageHero - Two-column hero section for Docusaurus homepage
 *
 * Left column: Title and subtitle text content
 * Right column: 3D humanoid robot scene
 *
 * Styled to match Docusaurus official docs aesthetic
 */
export default function HomepageHero() {
  return (
    <header className={clsx('hero hero--primary', styles.heroSection)}>
      <div className={clsx('container', styles.container)}>
        <div className={styles.grid}>
          {/* Left Column - Text Content */}
          <div className={styles.content}>
            <h1 className={clsx('hero__title', styles.title)}>
              Physical AI & Humanoid Robotics
            </h1>
            <p className={clsx('hero__subtitle', styles.subtitle)}>
              Bridging the gap between the digital brain and the physical body.
            </p>
            <div className={styles.buttons}>
              <a
                className={clsx(
                  'button button--primary button--lg',
                  styles.ctaButton
                )}
                href="/docs/intro"
              >
                Get Started
              </a>
              <a
                className={clsx(
                  'button button--secondary button--lg',
                  styles.secondaryButton
                )}
                href="/docs/robotics-module-one/index"
              >
                View Curriculum
              </a>
            </div>
          </div>

          {/* Right Column - 3D Robot Scene */}
          <div className={styles.robotScene}>
            <HeroRobot />
          </div>
        </div>
      </div>
    </header>
  );
}
