"use client";

import { ChangeEvent, DragEvent, useRef, useState } from "react";

import { useMutation, useQueryClient } from "@tanstack/react-query";

import { uploadDocument } from "@/lib/api/document";
import { ApiError } from "@/lib/api/client";

import { Button } from "@/components/ui/button";

const MAX_FILE_SIZE = 20 * 1024 * 1024;

interface DocumentUploadProps {
  onUploadSuccess?: () => void;
}

export function DocumentUpload({ onUploadSuccess }: DocumentUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const queryClient = useQueryClient();

  const [isDragging, setIsDragging] = useState(false);

  const [error, setError] = useState<string | null>(null);

  const [uploadedFilename, setUploadedFilename] = useState<string | null>(null);

  const uploadMutation = useMutation({
    mutationFn: uploadDocument,

    onSuccess: async (response) => {
      setError(null);
      setUploadedFilename(response.filename);

      await queryClient.invalidateQueries({
        queryKey: ["documents"],
      });

      onUploadSuccess?.();

      if (inputRef.current) {
        inputRef.current.value = "";
      }
    },

    onError: (uploadError: unknown) => {
      setUploadedFilename(null);

      if (uploadError instanceof ApiError) {
        setError(uploadError.message);
        return;
      }

      if (uploadError instanceof Error) {
        setError(uploadError.message);
        return;
      }

      setError("Failed to upload document.");
    },
  });

  function validateFile(file: File): string | null {
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      return "Only PDF files are allowed.";
    }

    if (file.size === 0) {
      return "The selected file is empty.";
    }

    if (file.size > MAX_FILE_SIZE) {
      return "The maximum file size is 20 MB.";
    }

    return null;
  }

  function handleFile(file: File) {
    setError(null);
    setUploadedFilename(null);

    const validationError = validateFile(file);

    if (validationError) {
      setError(validationError);
      return;
    }

    uploadMutation.mutate(file);
  }

  function handleInputChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];

    if (file) {
      handleFile(file);
    }
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setIsDragging(false);

    const file = event.dataTransfer.files?.[0];

    if (file) {
      handleFile(file);
    }
  }

  function handleDragOver(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    setIsDragging(true);
  }

  function handleDragLeave() {
    setIsDragging(false);
  }

  function openFilePicker() {
    inputRef.current?.click();
  }

  const isUploading = uploadMutation.isPending;

  return (
    <div>
      <div
        role="button"
        tabIndex={0}
        onClick={openFilePicker}
        onKeyDown={(event) => {
          if (event.key === "Enter" || event.key === " ") {
            openFilePicker();
          }
        }}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        className={[
          "cursor-pointer rounded-xl border-2 border-dashed p-10",
          "text-center transition",
          isDragging
            ? "border-white bg-slate-800"
            : "border-slate-700 bg-slate-900 hover:border-slate-500",
          isUploading ? "pointer-events-none opacity-70" : "",
        ].join(" ")}
      >
        <div className="mx-auto flex max-w-md flex-col items-center">
          <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-slate-800 text-2xl">
            {isUploading ? "⏳" : "📄"}
          </div>

          <h3 className="text-lg font-semibold">
            {isUploading ? "Processing PDF..." : "Upload a PDF"}
          </h3>

          <p className="mt-2 text-sm text-slate-400">
            {isUploading
              ? "Extracting text, creating chunks and embeddings."
              : "Drag and drop your PDF here, or click to browse."}
          </p>

          {!isUploading && (
            <p className="mt-1 text-xs text-slate-500">
              Maximum file size: 20 MB
            </p>
          )}

          <input
            ref={inputRef}
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleInputChange}
            className="hidden"
            disabled={isUploading}
          />
        </div>
      </div>

      {isUploading && (
        <div className="mt-4 h-1 overflow-hidden rounded-full bg-slate-800">
          <div className="h-full w-1/3 animate-pulse rounded-full bg-white" />
        </div>
      )}

      {uploadedFilename && (
        <div className="mt-4 rounded-lg border border-emerald-900 bg-emerald-950/30 p-4">
          <div className="flex items-start gap-3">
            <span className="text-emerald-400">✓</span>

            <div>
              <p className="text-sm font-medium text-emerald-300">
                Document processed successfully
              </p>

              <p className="mt-1 text-xs text-emerald-300/70">
                {uploadedFilename} is now available in your document library.
              </p>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-4 rounded-lg border border-red-900 bg-red-950/30 p-4">
          <div className="flex items-start gap-3">
            <span className="text-red-400">!</span>

            <div>
              <p className="text-sm font-medium text-red-300">Upload failed</p>

              <p className="mt-1 text-xs leading-5 text-red-300/70">{error}</p>
            </div>
          </div>
        </div>
      )}

      <div className="mt-4 flex justify-end">
        <Button
          type="button"
          variant="secondary"
          onClick={openFilePicker}
          disabled={isUploading}
        >
          {isUploading ? "Processing..." : "Choose PDF"}
        </Button>
      </div>
    </div>
  );
}
