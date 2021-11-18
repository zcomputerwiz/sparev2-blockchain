import React from 'react';
import { SvgIcon, SvgIconProps } from '@material-ui/core';
import { ReactComponent as replacemeIcon } from './images/replaceme.svg';

export default function Keys(props: SvgIconProps) {
  return <SvgIcon component={replacemeIcon} viewBox="0 0 150 58" {...props} />;
}
