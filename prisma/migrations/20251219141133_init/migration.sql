-- CreateEnum
CREATE TYPE "FaceAngle" AS ENUM ('FRONT', 'LEFT', 'RIGHT', 'UP', 'DOWN');

-- CreateTable
CREATE TABLE "Student" (
    "id" SERIAL NOT NULL,
    "fullName" TEXT NOT NULL,
    "studentId" TEXT NOT NULL,
    "schoolEmail" TEXT NOT NULL,
    "status" TEXT NOT NULL DEFAULT 'active',
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Student_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "FaceImage" (
    "id" SERIAL NOT NULL,
    "studentId" INTEGER NOT NULL,
    "angle" "FaceAngle" NOT NULL,
    "filePath" TEXT NOT NULL,
    "embedding" JSONB,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "FaceImage_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Student_studentId_key" ON "Student"("studentId");

-- CreateIndex
CREATE UNIQUE INDEX "Student_schoolEmail_key" ON "Student"("schoolEmail");

-- AddForeignKey
ALTER TABLE "FaceImage" ADD CONSTRAINT "FaceImage_studentId_fkey" FOREIGN KEY ("studentId") REFERENCES "Student"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
