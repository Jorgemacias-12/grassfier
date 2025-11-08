export interface ImageDimensions {
  width: number;
  height: number;
}

export interface ImageInfo {
  name: string;
  size: number;
  type: string;
  lastModified: number;
  dimensions: ImageDimensions;
}

export interface ImageData {
  url: string;
  file: File;
}

export interface PredicttionResult {
  label: string;
  confidence: number;
  message?: string;
}
