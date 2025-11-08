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

export interface Payload {
  message: string;
  image_info: ServerImageData;
  prediction?: string;
}

export interface ServerImageData {
  filename: string;
  content_type: string;
  file_size: number;
  image_format: string | null;
  image_size: string;
  image_mode: string;
}

export interface ApiResponse {
  success: boolean;
  data?: Payload;
  errors?: string[];
}
