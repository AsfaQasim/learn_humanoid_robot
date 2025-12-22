import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import FloatingChatIcon from '../components/FloatingChatIcon';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <FloatingChatIcon />
    </>
  );
}