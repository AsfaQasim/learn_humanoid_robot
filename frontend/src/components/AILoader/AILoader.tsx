import React from 'react';
import styles from './AILoader.module.css';

interface AILoaderProps {
  isVisible: boolean;
}

export default function AILoader({ isVisible }: AILoaderProps) {
  if (!isVisible) return null;

  return (
    <div className={styles.loaderContainer}>
      <div className={styles.circleWrapper}>
        <div className={styles.outerCircle}></div>
        <div className={styles.middleCircle}></div>
        <div className={styles.innerCircle}></div>
        <div className={styles.scanningLine}></div>
      </div>
      <div className={styles.loaderText}>
        <span>Initializing AI Robot</span>
        <div className={styles.dots}>
          <div className={styles.dot}></div>
          <div className={styles.dot}></div>
          <div className={styles.dot}></div>
        </div>
      </div>
    </div>
  );
}
