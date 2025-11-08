import type { ImageInfo, ImageData, ApiResponse } from "@/types";
import { X, Upload, AlertTriangle, CircleCheck, FileImage } from "lucide-react";
import { useState, useRef } from "react";

export const Classifier = () => {
  const [image, setImage] = useState<ImageData | null>(null);
  const [imageInfo, setImageInfo] = useState<ImageInfo | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);
  const [apiResponse, setApiResponse] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    const files = event.target.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (file.type.startsWith("image/")) processImageFile(file);
    }
  };

  const processImageFile = (file: File): void => {
    const reader = new FileReader();
    reader.onload = (e: ProgressEvent<FileReader>) => {
      if (e.target && typeof e.target.result === "string") {
        const img = new Image();
        img.onload = () => {
          setImage({ url: e.target!.result as string, file });
          setImageInfo({
            name: file.name,
            size: file.size,
            type: file.type,
            lastModified: file.lastModified,
            dimensions: { width: img.width, height: img.height },
          });
          setSuccess(true);
          setApiResponse(null);
          setError(null);
        };
        img.src = e.target.result as string;
      }
    };
    reader.readAsDataURL(file);
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>): void => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>): void => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>): void => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type.startsWith("image/")) {
      processImageFile(files[0]);
    }
  };

  const handleButtonClick = (): void => {
    fileInputRef.current?.click();
  };

  const handleRemoveImage = (): void => {
    setImage(null);
    setImageInfo(null);
    setSuccess(false);
    setApiResponse(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
  };

  const handlePredict = async (): Promise<void> => {
    if (!image) return;

    setLoading(true);
    setApiResponse(null);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", image.file);

      const res = await fetch("http://localhost:8000/api/predict", {
        method: "POST",
        body: formData,
      });

      const data: ApiResponse = await res.json();

      if (!data.success) {
        setError(data.errors?.join(", ") ?? "Error desconocido");
      } else {
        setApiResponse(data);
      }
    } catch (err) {
      setError("No se pudo conectar con el servidor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main id="classifier" className="py-20 md:py-32 bg-[#f4f6f4]">
      <section className="container flex flex-col gap-6 mx-auto px-4">
        <div className="max-w-4xl mx-auto text-center gap-2 flex flex-col">
          <h2 className="text-3xl md:text-4xl font-bold text-foreground">
            Clasificador de Enfermedades
          </h2>
          <p className="text-lg text-[#636363]">
            Carga una imagen de tu planta y obtén un análisis detallado en
            segundos
          </p>
        </div>

        <div className="max-w-4xl w-full h-auto mx-auto px-4 py-8 rounded-md flex flex-col md:flex-row items-center gap-4">
          <div
            className={`border-2 w-full gap-4 rounded-md border-dashed hover:border-[#0a6802]/50 cursor-pointer p-4 flex flex-col items-center justify-center bg-white shadow-md transition-all duration-200 ${
              isDragOver ? "border-[#0a6802] bg-[#f0f9ff]" : "border-[#d1d5db]"
            } ${image ? "min-h-[300px]" : "min-h-[250px]"}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={!image ? handleButtonClick : undefined}
          >
            {image ? (
              <div className="relative w-full h-full flex flex-col items-center justify-center">
                <div className="relative max-w-md w-full">
                  <img
                    src={image.url}
                    alt="Vista previa"
                    className="w-full h-auto max-h-48 object-contain rounded-lg shadow-sm"
                  />
                  <button
                    onClick={handleRemoveImage}
                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
                    type="button"
                    aria-label="Eliminar imagen"
                  >
                    <X size={16} />
                  </button>
                </div>
                <p className="text-sm text-[#0a6802] mt-3 font-medium">
                  Imagen cargada correctamente
                </p>
                <p className="text-xs text-[#636363] mt-1">
                  Haz clic en el área para cambiar la imagen
                </p>
              </div>
            ) : (
              <>
                <span
                  className={`w-fit p-2 inline-flex rounded-full transition-colors ${
                    isDragOver
                      ? "bg-[#0a6802] text-white"
                      : "text-[#0a6802] bg-[#0a6802]/10"
                  }`}
                >
                  <Upload size={32} />
                </span>

                <section className="text-center">
                  <h5 className="font-semibold text-foreground mb-1">
                    {isDragOver
                      ? "Suelta la imagen aquí"
                      : "Arrastra tu imagen aquí"}
                  </h5>
                  <p className="text-sm text-muted-foreground mb-4">
                    o haz clic para seleccionar
                  </p>
                </section>

                <button
                  className="inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-all h-9 px-4 py-2 bg-[#0a6802] hover:bg-[#0a6802]/90 text-white"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleButtonClick();
                  }}
                  type="button"
                >
                  Seleccionar archivo
                </button>

                <p className="text-sm text-[#636363]">PNG, JPG hasta 10 MiB</p>
              </>
            )}

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
            />
          </div>

          <hr className="w-full md:w-[1px] md:h-full border" />

          <div className="bg-white flex items-center flex-col gap-6 rounded-xl border p-8 w-full md:max-w-md">
            {loading ? (
              <div className="w-full text-center">
                <div className="animate-spin rounded-full h-10 w-10 border-4 border-[#0a6802]/40 border-t-[#0a6802] mx-auto mb-4"></div>
                <p className="text-[#636363] text-sm">Analizando imagen...</p>
              </div>
            ) : error ? (
              <div className="w-full text-center text-red-600">
                <AlertTriangle className="mx-auto mb-2" size={32} />
                <p className="text-sm">{error}</p>
              </div>
            ) : success && imageInfo ? (
              <div className="w-full">
                <div className="flex items-center gap-3 mb-6">
                  <CircleCheck color="#0a6802" size={32} />
                  <h3 className="text-lg font-semibold text-foreground">
                    Imagen lista para análisis
                  </h3>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-sm">
                    <FileImage size={16} className="text-[#636363]" />
                    <span className="font-medium">Nombre:</span>
                    <span
                      className="text-[#636363] truncate"
                      title={imageInfo.name}
                    >
                      {imageInfo.name}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 text-sm">
                    <span className="font-medium">Tamaño:</span>
                    <span className="text-[#636363]">
                      {formatFileSize(imageInfo.size)}
                    </span>
                  </div>

                  <div className="flex items-center gap-2 text-sm">
                    <span className="font-medium">Dimensiones:</span>
                    <span className="text-[#636363]">
                      {imageInfo.dimensions.width} ×{" "}
                      {imageInfo.dimensions.height}px
                    </span>
                  </div>
                </div>

                {!apiResponse ? (
                  <button
                    className="w-full mt-6 inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-all h-10 px-4 py-2 bg-[#0a6802] hover:bg-[#0a6802]/90 text-white"
                    type="button"
                    onClick={handlePredict}
                  >
                    Iniciar Análisis
                  </button>
                ) : (
                  <div className="mt-6 border-t pt-4">
                    <h4 className="text-base font-semibold text-foreground mb-2">
                      Resultado del análisis:
                    </h4>
                    <p className="text-sm text-[#0a6802] font-medium mb-1">
                      {apiResponse.data?.prediction ?? "Pendiente"}
                    </p>
                    <p className="text-xs text-[#636363]">
                      {apiResponse.data?.message ?? ""}
                    </p>
                  </div>
                )}
              </div>
            ) : (
              <>
                <CircleCheck color="#d0d0d0" size={48} />
                <p className="text-sm text-[#636363] text-center">
                  Carga una imagen para ver los resultados del análisis.
                </p>
              </>
            )}
          </div>
        </div>
      </section>
    </main>
  );
};
